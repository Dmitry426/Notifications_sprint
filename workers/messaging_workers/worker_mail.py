
import json
import logging
from abc import ABC

from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.exchange_type import ExchangeType
from pika.spec import Basic, BasicProperties

from workers.event_listeners.services.rabbit_consumer_base import RabbitConsumer
from workers.messaging_workers.services.mail_service import send_email

logger = logging.getLogger(__name__)


class WorkerConsumerMail(RabbitConsumer, ABC):
    exchange = "event"
    exchange_type = ExchangeType.direct
    queue = "ugc_notification.websocket"


class WorkerMail(WorkerConsumerMail, ABC):
    def __init__(self, read_connection: BlockingConnection):
        super().__init__(read_connection)

    def message_callback(self,
                         ch: BlockingChannel,
                         method: Basic.Ack,
                         properties: BasicProperties,
                         body: bytes) -> None:
        dict_body = json.loads(body)
        logger.info("Delivery properties: %s, message metadata: %s", method, properties)
        send_email(dict_body['subject'], dict_body['text'], dict_body['body'], dict_body['to'])
        logger.info(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_mailing(self) -> None:
        super(WorkerConsumerMail, self).consume()
