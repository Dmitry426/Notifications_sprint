import json
from services.workers import producer, consumer
from services.utils import get_html
from Configs.logger_notifications import logger


def on_message(ch, method, properties, body):
    """Called when a message is received. Log message and ack it."""
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

        letter = get_html(data, 'bookmarks.html')
        text = f"Приветствуем,{user['name']}\nновую серию «{dict_body['serial_name']}»" +\
               f".\nСерия доступна по ссылке:{dict_body['link']}"

        data = {"subject": f'Вышла новая серия сериала {dict_body["serial_name"]}',
                "text": text,
                "body": letter,
                "to": user['email']}
        data_json = json.dumps(data)
        producer(data_json, 'email')
    logger.info(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


consumer("ugc_notification", on_message)
