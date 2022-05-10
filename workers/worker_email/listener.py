import json
from services.workers import consumer
from services.utils import send_email
from Configs.logger_notifications import logger


def on_message(ch, method, properties, body):
    dict_body = json.loads(body)
    logger.info("Delivery properties: %s, message metadata: %s", method, properties)
    logger.info("Message body: %s", dict_body)
    logger.info(" [x] Received %r" % (dict_body,))
    logger.info(f"\n\nНаше письмо ушло\n{dict_body['to']}\n\n")
    send_email(dict_body['subject'], dict_body['text'], dict_body['body'], dict_body['to'])

    logger.info(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


consumer("email", on_message)
