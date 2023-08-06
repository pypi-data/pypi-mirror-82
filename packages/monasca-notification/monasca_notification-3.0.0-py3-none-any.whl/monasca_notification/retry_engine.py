# (C) Copyright 2015-2016 Hewlett Packard Enterprise Development LP
# Copyright 2017 Fujitsu LIMITED
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time

from oslo_config import cfg
from oslo_log import log as logging
from oslo_serialization import jsonutils

from monasca_common.kafka import client_factory
from monasca_notification.common.utils import construct_notification_object
from monasca_notification.common.utils import get_db_repo
from monasca_notification.common.utils import get_statsd_client
from monasca_notification.processors import notification_processor

log = logging.getLogger(__name__)
CONF = cfg.CONF


class RetryEngine(object):
    def __init__(self):
        self._statsd = get_statsd_client()

        self._consumer = client_factory.get_kafka_consumer(
            CONF.kafka.url,
            CONF.kafka.group,
            CONF.kafka.notification_retry_topic,
            CONF.zookeeper.url,
            CONF.zookeeper.notification_retry_path,
            CONF.kafka.legacy_kafka_client_enabled)
        self._producer = client_factory.get_kafka_producer(
            CONF.kafka.url,
            CONF.kafka.legacy_kafka_client_enabled)

        self._notifier = notification_processor.NotificationProcessor()
        self._db_repo = get_db_repo()

    def run(self):
        for raw_notification in self._consumer:
            message = raw_notification.value()
            notification_data = jsonutils.loads(message)

            notification = construct_notification_object(self._db_repo, notification_data)

            if notification is None:
                self._consumer.commit()
                continue

            wait_duration = CONF.retry_engine.interval - (
                time.time() - notification_data['notification_timestamp'])

            if wait_duration > 0:
                time.sleep(wait_duration)

            sent, failed = self._notifier.send([notification])

            if sent:
                self._producer.publish(CONF.kafka.notification_topic,
                                       [notification.to_json()])

            if failed:
                notification.retry_count += 1
                notification.notification_timestamp = time.time()
                if notification.retry_count < CONF.retry_engine.max_attempts:
                    log.error(u"retry failed for {} with name {} "
                              u"at {}.  "
                              u"Saving for later retry.".format(notification.type,
                                                                notification.name,
                                                                notification.address))
                    self._producer.publish(CONF.kafka.notification_retry_topic,
                                           [notification.to_json()])
                else:
                    log.error(u"retry failed for {} with name {} "
                              u"at {} after {} retries.  "
                              u"Giving up on retry."
                              .format(notification.type,
                                      notification.name,
                                      notification.address,
                                      CONF.retry_engine.max_attempts))

            self._consumer.commit()
