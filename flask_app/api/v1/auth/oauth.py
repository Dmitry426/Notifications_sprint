import os
import requests

from app import app, oauth
from config import TypeSocial
from flask import url_for, request
from flask_app.api.v1.auth.base import get_token_social_data
from flask_app.utils.rate_limit import rate_limit
from http import HTTPStatus


@app.route('/login/<service_name>')
@rate_limit()
def log_in(service_name):
    service = oauth.create_client(service_name)
    if service_name == TypeSocial.yandex.value:
        redirect_uri = url_for('authorize_yandex', _external=True)
    elif service_name == TypeSocial.google.value:
        redirect_uri = url_for('authorize_google', _external=True)
    else:
        return {'message': f'{service_name} не обслуживается'}, HTTPStatus.NOT_FOUND
    return service.authorize_redirect(redirect_uri)


@app.route('/authorize_yandex')
@rate_limit()
def authorize_yandex():
    # первый способ
    code = request.args['code']
    client_id = os.getenv('YANDEX_CLIENT_ID'),
    client_secret = os.getenv('YANDEX_CLIENT_SECRET')
    yandex_response = requests.post(
        url=os.getenv('YANDEX_URL_TOKEN'),
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
        },
    ).json()
    access_token = yandex_response.get("access_token")
    user_info_response = requests.get(
        url=os.getenv('YANDEX_URL_INFO'),
        params={
            "format": "json",
            "with_openid_identity": 1,
            "oauth_token": access_token,
        },
    ).json()
    result = get_token_social_data(user_info_response.get("login"), user_info_response.get("default_email"))
    return result


@app.route('/authorize_google')
@rate_limit()
def authorize_google():
    # второй способ
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    google_user = token.get("userinfo")
    if not google_user:
        google_user = google.userinfo()
    result = get_token_social_data(google_user.name, google_user.email)
    return result
