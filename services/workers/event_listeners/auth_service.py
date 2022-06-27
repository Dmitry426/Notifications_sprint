import json
import logging
from abc import ABC

from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.exchange_type import ExchangeType
from pika.spec import Basic, BasicProperties

from .models.auth_event import UserAuth, WellcomeLetter
from .services.base_services import BasicTemplating
from .services.rabbit_consumer_base import RabbitConsumer
from .services.rabbit_producer_base import RabbitPublisher

logger = logging.getLogger("auth_service")


class AuthConsumerBase(RabbitConsumer, ABC):
    exchange = "event"
    exchange_type = ExchangeType.direct
    queue = "auth_notification"


class AuthProducerBase(RabbitPublisher, ABC):
    exchange = "delivery"
    exchange_type = ExchangeType.direct
    queue = "email"


class ConsumerAuth(AuthConsumerBase, BasicTemplating):
    def __init__(
        self, write_connection: BlockingConnection, read_connection: BlockingConnection
    ):
        super().__init__(read_connection)
        self._connection = write_connection
        self._producer = AuthProducerBase(self._connection)

    def message_callback(
        self,
        ch: BlockingChannel,
        method: Basic.Ack,
        properties: BasicProperties,
        body: bytes,
    ) -> None:
        dict_body = UserAuth(**json.loads(body))
        logger.info(
            " Delivery properties: %s, message metadata: %s", method, properties
        )
        letter = self.get_template(dict_body.dict(), template_name="welcome.html")
        text = """Приветствуем,'%s'\nСкопируйте и вставьте следующий адрес"
             в свой веб-браузер: '%s' """ % (
            dict_body.user,
            dict_body.link,
        )

        data = WellcomeLetter(body=letter, text=text, to=dict_body.email)
        self._producer.produce(body=data.to_json())
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_auth(self):
        super(AuthConsumerBase, self).consume()
