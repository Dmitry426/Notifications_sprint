__all__ = ["BasicTemplating", "insert_notification"]

import json
import os
import requests
from urllib.parse import urljoin


import bitly_api
from jinja2 import select_autoescape, Environment, FileSystemLoader

from workers.event_listeners.core.config import settings
from workers.event_listeners.models.websocket_postgres import UserWebsock


class BasicTemplating:
    @staticmethod
    def get_template(data: dict, template_name: str) -> str:
        env = Environment(
            loader=FileSystemLoader(os.path.join('/', 'src/templates')),
            autoescape=select_autoescape(["html", "xml"]),
        )
        template = env.get_template(template_name)
        rendered = template.render(data)
        return rendered

    @staticmethod
    def little_url(url):
        access = bitly_api.Connection(access_token=settings.bitly_access_token)
        short_url = access.shorten(url)
        return short_url['url']

    @staticmethod
    def get_data(url: str, user_id: str) -> json:
        response = requests.get(urljoin(url, user_id))
        return response.json()


async def insert_notification(postgres_connect, data: json) -> str:
    conn = await postgres_connect()
    message = UserWebsock(**data)
    print(message.body)
    print(type(message.user_id))
    sql = f"""insert into events.notifications
                  ( user_id, body) VALUES
                   ( '%s' , '%s' ) """ % (message.user_id, message.body)

    try:
        return await conn.execute(sql)
    finally:
        await conn.close()
