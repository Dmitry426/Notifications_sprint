import json

import pika
from pika import BlockingConnection

from workers.event_listeners.core.config import settings


def rabbit_conn_consume() -> BlockingConnection:
    credentials = pika.PlainCredentials(
        username=settings.r_name, password=settings.r_password
    )
    parameters = pika.ConnectionParameters(
        host="localhost", credentials=credentials, virtual_host="/vhost1"
    )

    connection_rabbit = pika.BlockingConnection(parameters)
    return connection_rabbit


def producer(body, queue):
    channel = rabbit_conn_consume().channel()
    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=2,
        ),
    )
    print("done")
    rabbit_conn_consume().close()


# welcome
link = "https://bit.ly/3kLZMwf"
user = "Иван Иванов"
email = "1225@kartgeocentre.ru"
data = {
    "link_out": "https://pastseason.ru/",
    "link": link,
    "user": user,
    "email": email,
}
data_json = json.dumps(data)
producer(data_json, "auth_notification")

# #bookmarks
data = {
    "link_out": "https://pastseason.ru/",
    "link": "http://pastseason.ru/serial/Band.of.Brothers",
    "users": [
        {"name": "Иван петрович Иванов", "email": "1213@kartgeocentre.ru"},
        {"name": "Петр Иванович Петров", "email": "1214@kartgeocentre.ru"},
        {"name": "Василий Васильевич Васильев", "email": "1215@kartgeocentre.ru"},
    ],
    "serial_name": "Братья по оружию",
}
data_json = json.dumps(data)
producer(data_json, "ugc_notification")

# websocket
data = {
    "user_id": "e703065e-25e1-45fe-9bc6-ddacc30ca239",
    "body": "Пользователь создан",
}
data_json = json.dumps(data)
producer(data_json, "ugc_notification.websocket")
data = {
    "user_id": "e703065e-25e1-45fe-9bc6-ddacc30ca239",
    "body": "Пользователь Читает X-box",
}
data_json = json.dumps(data)
producer(data_json, "ugc_notification.websocket")
