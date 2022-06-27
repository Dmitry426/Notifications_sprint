__all__ = ["send_email"]

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..core.config import settings

FROM_MAIL = settings.mail.email_from
MAIL_PASSWORD = settings.mail.password
MAIL_SMTP = settings.mail.smtp
MAIL_SMTP_PORT = settings.mail.smtp_port


def send_email(subject, text, body, to):
    msg = MIMEMultipart("alternative")
    msg["subject"] = subject
    msg["to"] = to
    msg["from"] = FROM_MAIL

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(body, "html")

    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP(MAIL_SMTP, MAIL_SMTP_PORT)
    server.ehlo()
    server.starttls()
    server.login(FROM_MAIL, MAIL_PASSWORD)
    server.sendmail(FROM_MAIL, to, msg.as_string())

    server.quit()
