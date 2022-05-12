import json
from services.workers import producer, consumer
from services.utils import get_html
from Configs.logger_notifications import logger


def on_message(ch, method, properties, body):
    dict_body = json.loads(body)
    logger.info("Delivery properties: %s, message metadata: %s", method, properties)
    logger.info("Message body: %s", dict_body)
    logger.info(" [x] Received %r" % (dict_body,))
    letter = get_html(dict_body, 'welcome.html')
    text = f"Приветствуем,{dict_body['user']}\nСкопируйте и вставьте следующий адрес" +\
           f" в свой веб-браузер: {dict_body['link']}"

    data = {"subject": 'Welcome letter',
            "text": text,
            "body": letter,
            "to": dict_body['email']}
    data_json = json.dumps(data)
    producer(data_json, 'email')
    logger.info(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


consumer("auth_notification", on_message)
