import json
from services.workers import producer, consumer
from services.utils import get_html, send_email


# welcome
link = 'https://bit.ly/3kLZMwf'
user = 'Иван Иванов'
email = '202@kartgeocentre.ru'
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
        {'name': 'Иван петрович Иванов', 'email': "200@kartgeocentre.ru"},
        {'name': 'Петр Иванович Петров', 'email': "201@kartgeocentre.ru"}
    ],
    'serial_name': 'Братья по оружию'
}

data_json = json.dumps(data)
producer(data_json, 'ugc_notification')


# #bookmarks
# data = {
#     'link_out': 'https://pastseason.ru/',
#     'link': 'http://pastseason.ru/serial/Band.of.Brothers',
#     'users': [
#         {'name': 'Иван петрович Иванов', 'email': "113@kartgeocentre.ru"},
#         {'name': 'Петр Иванович Петров', 'email': "114@kartgeocentre.ru"},
#         {'name': 'Василий Васильевич Васильев', 'email': "115@kartgeocentre.ru"}
#     ],
#     'serial_name': 'Братья по оружию'
# }
#
# data_json = json.dumps(data)
# producer(data_json, 'ugc_notification')

