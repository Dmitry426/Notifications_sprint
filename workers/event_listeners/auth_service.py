import json
import logging
from abc import ABC

from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.exchange_type import ExchangeType
from pika.spec import Basic, BasicProperties

from workers.event_listeners.models.auth_event import UserAuth, WellcomeLetter
from workers.event_listeners.services.base_services import BasicTemplating
from workers.event_listeners.services.rabbit_consumer_base import RabbitConsumer
from workers.event_listeners.services.rabbit_producer_base import RabbitPublisher

logger = logging.getLogger(__name__)


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
            "None - Delivery properties: %s, message metadata: %s", method, properties
        )
        letter = self.get_template(dict_body.dict(), template_name="welcome.html")
        text = """Приветствуем,'%s'\nСкопируйте и вставьте следующий адрес"
             в свой веб-браузер: '%s' """ % (
            dict_body.user,
            dict_body.link,
        )

        data = WellcomeLetter(body=letter, text=text, to=dict_body.email)
        self._producer.produce(body=data.to_json())
        logger.info("None - Message is templated ")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_auth(self):
        super(AuthConsumerBase, self).consume()
