import json
import os
import requests
from urllib.parse import urljoin

import bitly_api
from jinja2 import select_autoescape, Environment, PackageLoader, FileSystemLoader

from workers.event_listeners.core.config import settings


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
