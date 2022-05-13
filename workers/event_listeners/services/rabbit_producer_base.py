__all__ = ["RabbitPublisher"]

import logging
from abc import ABC, abstractmethod

import backoff
import pika
from pika import BlockingConnection
from pika.exceptions import AMQPConnectionError
from pika.exchange_type import ExchangeType

from workers.event_listeners.core.config import settings

logger = logging.getLogger(__name__)


class RabbitPublisher(ABC):
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

    def __init__(self, producer_connection: BlockingConnection):
        self.producer_connection = producer_connection

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(RuntimeError, TimeoutError, AMQPConnectionError),
        max_time=settings.max_backoff,
    )
    def produce(self, body: bytes):
        channel = self.producer_connection.channel()
        properties = pika.BasicProperties(delivery_mode=2)
        channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.queue,
            body=body,
            properties=properties,
        )
        logger.info("None -  Данные отправлены")
        channel.close()
