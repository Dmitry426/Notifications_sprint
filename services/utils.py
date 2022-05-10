__all__ = ["send_email", "get_html", "little_url"]

import os
import bitly_api
import smtplib

from Configs import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, select_autoescape, FileSystemLoader
from Configs.logger_notifications import logger

TEMPLATE_ROOT = os.path.join('/', 'templates')
logger.info(f'\n\n\n---13---{TEMPLATE_ROOT}\n\n\n')
env = Environment(
    loader=FileSystemLoader(TEMPLATE_ROOT),
    autoescape=select_autoescape(['html', 'xml'])
)

FROM_MAIL = config.settings.from_mail
MAIL_PASSWORD = config.settings.mail_password
MAIL_SMTP = config.settings.mail_smtp
MAIL_SMTP_PORT = config.settings.mail_smtp_port
BITLY_ACCESS_TOKEN = config.settings.bitly_access_token


def send_email(subject, text, body, to):
    msg = MIMEMultipart('alternative')
    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = FROM_MAIL

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(body, 'html')

    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP(MAIL_SMTP, MAIL_SMTP_PORT)
    server.ehlo()
    server.starttls()
    server.login(FROM_MAIL, MAIL_PASSWORD)
    server.sendmail(FROM_MAIL, to, msg.as_string())

    server.quit()


def get_html(data, file_name):
    template = env.get_template(file_name)
    rendered = template.render(data)
    return rendered


def little_url(url):
    access = bitly_api.Connection(access_token=BITLY_ACCESS_TOKEN)
    short_url = access.shorten(url)
    return short_url['url']




# data_confirm_email = {
#     'link_out': 'https://pastseason.ru/',
#     'link': 'this_is_link_for_confirm_email',
#     'user': 'Иван иванович Иванов'
# }
# data_bookmarks = {
#     'link_out': 'https://pastseason.ru/',
#     'link': 'this_is_link_new_series',
#     'user': 'Иван петрович Иванов',
#     'serial_name': 'Санта-Барбара'
# }
# data_individual_letter = {
#     'link_out': 'https://pastseason.ru/',
#     'link': 'this_is_link_new_series',
#     'user': 'Иван васильевич Иванов',
#     'message_body': 'Здесь может быть любая чушь от менеджера'
# }
#
# data_personal_selection = {
#     'link_out': 'https://pastseason.ru/',
#     'link': 'this_is_link_new_series',
#     'user': 'Иван михайлович Иванов',
#     'selection': 'Здесь должна быть крутая подборка'
# }
#
# data_tip = {
#     'link_out': 'https://pastseason.ru/',
#     'link': 'this_is_link_new_series',
#     'user': 'Иван геннадьевич Иванов',
#     'movie_name': 'Грань будущего II',
#     'poster': 'Картинка, описание и т.п.',
#     'link_movie': 'link_to_movie'
# }
#
# data_statistics = {
#     'link_out': 'https://pastseason.ru/',
#     'link': 'this_is_link_new_series',
#     'user': 'Иван сергеевич Иванов',
#     'count_movies': '13',
#     'count_serials': '7',
#     'month': 'мае',
#     'count_films': '11',
#     'count_genre_max': '9',
#     'genre_max': 'фантастика'
# }


# print(get_html(data_confirm_email, 'welcome.html'))
# print(get_html(data_bookmarks, 'bookmarks.html'))
# print(get_html(data_individual_letter, 'mail.html'))
# print(get_html(data_personal_selection, 'personal_selection.html'))
# print(get_html(data_tip, 'tip.html'))
# print(get_html(data_statistics, 'statistics.html'))
