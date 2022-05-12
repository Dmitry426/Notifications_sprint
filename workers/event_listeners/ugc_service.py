import json
import logging
from abc import ABC

from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.exchange_type import ExchangeType
from pika.spec import Basic, BasicProperties

from workers.event_listener.services.rabbit_consumer_base import RabbitConsumer
from workers.event_listener.services.rabbit_producer_base import RabbitPublisher
from workers.event_listener.services.templating_service import BasicTemplating

logger = logging.getLogger(__name__)


class AuthConsumerBase(RabbitConsumer, ABC):
    exchange = "event"
    exchange_type = ExchangeType.direct
    queue = "ugc_notification"


class AuthProducerBase(RabbitPublisher, ABC):
    exchange = "delivery"
    exchange_type = ExchangeType.direct
    queue = "email"


class ConsumerUgc(AuthConsumerBase, BasicTemplating, ABC):
    def __init__(self, write_connection: BlockingConnection,
                 read_connection: BlockingConnection):
        super().__init__(read_connection)
        self._connection = write_connection
        self._producer = AuthProducerBase(self._connection)

    def message_callback(self,
                         ch: BlockingChannel,
                         method: Basic.Ack,
                         properties: BasicProperties,
                         body: bytes) -> None:
        dict_body = json.loads(body)
        logger.info("Delivery properties: %s, message metadata: %s", method, properties)
        logger.info("Message body: %s", dict_body)
        logger.info(" [x] Received %r" % (dict_body,))
        for user in dict_body['users']:
            data = {
                'link_out': dict_body['link_out'],
                'link': dict_body['link'],
                'user': user['name'],
                'serial_name': dict_body['serial_name']
            }

            letter = self.get_template(data, 'bookmarks.html')
            text = f"Приветствуем,{user['name']}\nновую серию «{dict_body['serial_name']}»" + \
                   f".\nСерия доступна по ссылке:{dict_body['link']}"

            data = {
                "subject": f'Вышла новая серия сериала {dict_body["serial_name"]}',
                "text": text,
                "body": letter,
                "to": user['email']
            }
            data_json = json.dumps(data)
            self._producer.produce(body=data_json.encode("utf-8"))
        logger.info(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_ugc(self):
        super(AuthConsumerBase, self).consume()
