import json

from services.workers import producer
from Configs import config

DB_NAME = config.settings.db_name
DB_USER = config.settings.db_user
DB_PASSWORD = config.settings.db_password
DB_HOST = config.settings.db_host
DB_PORT = config.settings.db_port

# welcome
link = 'https://bit.ly/3kLZMwf'
user = 'Иван Иванов'
email = '1225@kartgeocentre.ru'
data = {
    'link_out': 'https://pastseason.ru/',
    'link': link,
    'user': user,
    'email': email
}
data_json = json.dumps(data)
producer(data_json, 'auth_notification')

# #bookmarks
data = {
    'link_out': 'https://pastseason.ru/',
    'link': 'http://pastseason.ru/serial/Band.of.Brothers',
    'users': [
        {'name': 'Иван петрович Иванов', 'email': "1213@kartgeocentre.ru"},
        {'name': 'Петр Иванович Петров', 'email': "1214@kartgeocentre.ru"},
        {'name': 'Василий Васильевич Васильев', 'email': "1215@kartgeocentre.ru"}
    ],
    'serial_name': 'Братья по оружию'
}
data_json = json.dumps(data)
producer(data_json, 'ugc_notification')

#websocket
data = {"user_id": "e703065e-25e1-45fe-9bc6-ddacc30ca239",
        "body": "Пользователь создан"}
data_json = json.dumps(data)
producer(data_json, 'ugc_notification.websocket')
data = {"user_id": "e703065e-25e1-45fe-9bc6-ddacc30ca239",
        "body": "Пользователь Читает X-box"}
data_json = json.dumps(data)
producer(data_json, 'ugc_notification.websocket')
