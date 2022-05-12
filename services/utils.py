__all__ = ["send_email", "get_html", "little_url"]

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import bitly_api
from jinja2 import Environment, select_autoescape, FileSystemLoader

from Configs import config

TEMPLATE_ROOT = os.path.join('/', 'templates')
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
