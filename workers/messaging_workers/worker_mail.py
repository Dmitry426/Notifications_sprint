__all__ = ["WorkerMail"]

import json
import logging
from abc import ABC

from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.exchange_type import ExchangeType
from pika.spec import Basic, BasicProperties

from workers.messaging_workers.models.base import Letter
from workers.messaging_workers.services.mail_service import send_email
from workers.messaging_workers.services.rabbit_consumer_base import RabbitConsumer

logger = logging.getLogger(__name__)


class WorkerConsumerMail(RabbitConsumer, ABC):
    exchange = "delivery"
    exchange_type = ExchangeType.direct
    queue = "email"


class WorkerMail(WorkerConsumerMail):
    def __init__(self, read_connection: BlockingConnection):
        super().__init__(read_connection)

    def message_callback(
        self,
        ch: BlockingChannel,
        method: Basic.Ack,
        properties: BasicProperties,
        body: bytes,
    ) -> None:
        dict_body = Letter(**json.loads(body))
        logger.info("Delivery properties: %s, message metadata: %s", method, properties)
        send_email(
            subject=dict_body.subject,
            text=dict_body.text,
            body=dict_body.body,
            to=dict_body.to,
        )
        logger.info(" None - message is sent ")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_mailing(self) -> None:
        super(WorkerConsumerMail, self).consume()
