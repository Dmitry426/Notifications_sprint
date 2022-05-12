__all__ = ["RabbitConsumer"]

import logging

from abc import abstractmethod
import backoff

from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.exceptions import AMQPConnectionError
from pika.exchange_type import ExchangeType
from pika.spec import Basic

logger = logging.getLogger(__name__)


class RabbitConsumer(object):
    @property
    @abstractmethod
    def exchange(self) -> str:
        pass

    @property
    @abstractmethod
    def exchange_type(self) -> ExchangeType:
        pass

    @property
    @abstractmethod
    def queue(self) -> str:
        pass

    def __init__(self, consumer_connection: BlockingConnection):
        self.consumer_connection = consumer_connection
        self.channel = None

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(RuntimeError, TimeoutError, AMQPConnectionError),
        max_time=30,
    )
    def consume(self) -> None:
        self.channel = self.consumer_connection.channel()
        self.channel.basic_consume(queue=self.queue,
                                   on_message_callback=self.message_callback)
        self.connection_start()

    def connection_start(self) -> None:
        logger.info(' [*] Waiting for messages')
        self.channel.start_consuming()

    def close_connection(self) -> None:
        logger.info(' [*] Connection stopped  ')
        self.channel.close()

    @abstractmethod
    def message_callback(self,
                         ch: BlockingChannel,
                         method: Basic.Ack,
                         properties: BasicProperties,
                         body: bytes) -> None:
        pass
