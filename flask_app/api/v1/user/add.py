import json

from app import app, ma
from flask import request
from flask_app.api.v1.auth.base import generate_confirmation_token
from flask_app.db.postgresql import db
from flask_app.models.models import Role, User
from flask_app.schemas.user import user_create_schema, user_schema
from flask_app.utils.rate_limit import rate_limit
from flask_app.utils.welcome import get_html, little_url, send_email
from flask_app.utils.workers import producer
from http import HTTPStatus


@app.route('/users/add', methods=['POST'])
@rate_limit()
def user_add():
    """
        Создание пользователя
        ---
        tags:
          - Users
        parameters:
        - in: 'body'
          name: 'body'
          description: 'Укажите логин, электронную почту и пароль'
          required: 'true'
          schema:
            type: 'UserCreateSchema'
            schema:
              type: 'object'
              properties:
                password:
                  type: 'string'
                worker_email:
                  type: 'string'
                username:
                  type: 'string'
            example: {
                'username':'tester',
                'email': 'maild09@mail.ru',
                'password': '123123'
            }
        responses:
          201:
            description: Пользователь создан
            schema:
              type: 'object'
              properties:
                created:
                  type: 'string'
                  format: 'date-time'
                worker_email:
                  type: 'string'
                id:
                  type: 'string'
                last_changed:
                  type: 'string'
                  format: 'date-time'
                roles:
                  type: 'object'
                status:
                  type: 'boolean'
                username:
                  type: 'string'
          404:
            description: Данные не предоставлены.
          409:
            description: Такой пользователь уже существует. Попробуйте другое имя.
                         Такой worker_email уже используется. Попробуйте другой.
          422:
            description: Данные невалидны.
          429:
            description: Слишком много запросов с одного ip-адреса. Limit limit in interval seconds.
    """

    schema_view = user_schema
    schema_make = user_create_schema
    json_data = request.json
    if not json_data:
        return {'message': f'Данные не предоставлены.'}, HTTPStatus.NOT_FOUND
    try:
        new_user = schema_make.load(json_data, session=db.session)
    except Exception:
        return {'message': f'Данные невалидны.'}, HTTPStatus.UNPROCESSABLE_ENTITY

    schema_make.validate_username(new_user.username)
    schema_make.validate_email(new_user.email)

    new_user.status = False
    new_user.roles.append(db.session.query(Role).filter_by(title='authenticated user').first())

    db.session.add(new_user)
    db.session.commit()

    user = db.session.query(User).filter_by(email=new_user.email).first()

    token = generate_confirmation_token(user.id, user.email)

    confirm_url = f'http://127.0.0.1/confirm/{token}'
    link = little_url(confirm_url)

    data_confirm_email = {
        'link_out': 'https://pastseason.ru/',
        'link': link,
        'user': user.username,
        'email': user.email
    }

    try:
        data_json = json.dumps(data_confirm_email)
        producer(data_json, 'auth_notification')
        # print('\n\nЗапись в очередь\n\n')
    except:
        # На случай прямой отправки письма
        # print('\n\nСамостоятельная отправка письма\n\n')
        subject = 'Welcome Email'
        text = f"Приветствуем,{user.username}\nСкопируйте и вставьте следующий адрес в свой веб-браузер: {link}"
        body = get_html(data_confirm_email, 'welcome.html')
        # print("\n\n --пока не отправляем--\n\n")
        send_email(subject, text, body, user.email)
    return schema_view.dump(new_user), HTTPStatus.CREATED
