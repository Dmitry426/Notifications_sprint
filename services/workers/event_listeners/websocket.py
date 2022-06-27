import asyncio
import json
import logging
from abc import ABC

from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.exchange_type import ExchangeType
from pika.spec import Basic, BasicProperties

from .services.base_services import insert_notification
from .services.rabbit_consumer_base import RabbitConsumer

logger = logging.getLogger("websocket_service")


class UgcConsumerWebsocket(RabbitConsumer, ABC):
    exchange = "event"
    exchange_type = ExchangeType.direct
    queue = "ugc_notification.websocket"


class ConsumerUgcWebsock(UgcConsumerWebsocket):
    def __init__(self, read_connection: BlockingConnection, postgres_connection):
        super().__init__(read_connection)
        self._postgres_conn = postgres_connection

    def message_callback(
        self,
        ch: BlockingChannel,
        method: Basic.Ack,
        properties: BasicProperties,
        body: bytes,
    ) -> None:
        """Called when a message is received. Log message and ack it."""
        dict_body = json.loads(body)
        logger.info("Delivery properties: %s, message metadata: %s", method, properties)

        asyncio.run(
            insert_notification(postgres_connect=self._postgres_conn, data=dict_body)
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_ugc(self) -> None:
        super(UgcConsumerWebsocket, self).consume()
