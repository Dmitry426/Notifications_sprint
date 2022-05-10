import json
from services.workers import producer, consumer
from services.utils import get_html, send_email


# welcome
link = 'https://bit.ly/3kLZMwf'
user = 'Иван Иванов'
email = '225@kartgeocentre.ru'
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
        {'name': 'Иван петрович Иванов', 'email': "213@kartgeocentre.ru"},
        {'name': 'Петр Иванович Петров', 'email': "214@kartgeocentre.ru"},
        {'name': 'Василий Васильевич Васильев', 'email': "215@kartgeocentre.ru"}
    ],
    'serial_name': 'Братья по оружию'
}

data_json = json.dumps(data)
producer(data_json, 'ugc_notification')

