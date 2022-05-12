import logging

from abc import abstractmethod
import backoff
import pika
from pika import BlockingConnection
from pika.exceptions import AMQPConnectionError
from pika.exchange_type import ExchangeType

logger = logging.getLogger(__name__)


class RabbitPublisher(object):
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
        self.channel = None

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(RuntimeError, TimeoutError, AMQPConnectionError),
        max_time=30,
    )
    def produce(self, body:bytes) -> None:
        self.channel = self.producer_connection.channel()
        properties = pika.BasicProperties(
            delivery_mode=2
        )
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=self.queue,
                                   body=body,
                                   properties=properties,
                                   )
        logger.info("\n\n [x] Данные отправлены\n\n")
        self.channel.close()
