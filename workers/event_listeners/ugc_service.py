import json
import logging
from abc import ABC

from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.exchange_type import ExchangeType
from pika.spec import Basic, BasicProperties

from workers.event_listeners.models.base import Letter
from workers.event_listeners.models.ugc_event import Bookmark, BookmarkTemplateData
from workers.event_listeners.services.base_services import BasicTemplating
from workers.event_listeners.services.rabbit_consumer_base import RabbitConsumer
from workers.event_listeners.services.rabbit_producer_base import RabbitPublisher

logger = logging.getLogger(__name__)


class UgcConsumerBase(RabbitConsumer, ABC):
    exchange = "event"
    exchange_type = ExchangeType.direct
    queue = "ugc_notification"


class AuthProducerBase(RabbitPublisher, ABC):
    exchange = "delivery"
    exchange_type = ExchangeType.direct
    queue = "email"


class ConsumerUgc(UgcConsumerBase, BasicTemplating, ABC):
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
        dict_body = Bookmark(**json.loads(body))
        logger.info(
            "None - Delivery properties: %s, message metadata: %s", method, properties
        )

        for user in dict_body.users:
            data_template = BookmarkTemplateData(
                user=user.name,
                link=dict_body.link,
                link_out=dict_body.link_out,
                serial_name=dict_body.serial_name,
            )

            letter = self.get_template(data_template.dict(), "bookmarks.html")
            text = (
                f"Приветствуем, {user.name}\n"
                + f" Вышла новая серия сериала «{dict_body.serial_name}»"
                + f".\nСерия доступна по ссылке:{dict_body.link}"
            )
            greet = f"Вышла новая серия сериала {dict_body.serial_name}"
            data = Letter(subject=greet, body=letter, text=text, to=user.email)
            self._producer.produce(body=data.to_json())
        logger.info("None - Message is templated ")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_ugc(self) -> None:
        super(UgcConsumerBase, self).consume()
