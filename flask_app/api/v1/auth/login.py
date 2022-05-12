from app import app, ma, jwt
from flask import request
from flask_app.schemas.user import user_create_schema
from flask_app.db.postgresql import db
from flask_app.models.models import User
from flask_app.api.v1.auth.base import get_tokens
from flask_app.utils.rate_limit import rate_limit
from http import HTTPStatus


@app.route('/auth', methods=['POST'])
@rate_limit()
def login():
    """
        Авторизация пользователя
        ---
        tags:
          - Auth
        parameters:
        - in: 'body'
          name: 'body'
          description: 'Укажите логин и пароль'
          required: 'true'
          schema:
            type: 'UserCreateSchema'
            schema:
              type: 'object'
              properties:
                password:
                  type: 'string'
                email:
                  type: 'string'
                username:
                  type: 'string'
            example: {
                'username':'tester',
                'password': '123123'
            }
        responses:
          200:
            description: Пользователь авторизован
            schema:
              type: 'object'
              properties:
                access_token:
                  type: 'string'
                message:
                  type: 'string'
                refresh_token:
                  type: 'string'
          401:
            description: Неверные учетные данные.
          404:
            description: Данные не предоставлены.
          409:
            description: Такой пользователь уже существует. Попробуйте другое имя.
                         Такой email уже используется. Попробуйте другой.
          422:
            description: Данные невалидны.
          429:
            description: Слишком много запросов с одного ip-адреса. Limit limit in interval seconds.
    """
    schema_make = user_create_schema
    json_data = request.json
    if not json_data:
        return {'message': f'Данные не предоставлены.'}, HTTPStatus.NOT_FOUND
    try:
        prospect_user = schema_make.load(json_data, session=db.session)
    except ma.exception.ValidationError:
        return {'message': f'Данные невалидны.'}, HTTPStatus.UNPROCESSABLE_ENTITY
    login_user = db.session.query(User).filter_by(username=prospect_user.username).first()
    if not login_user:
        return {'message': f'Пользователя {prospect_user.username} не существует.'}, HTTPStatus.UNAUTHORIZED
    if login_user.password != prospect_user.password:
        return {'message': f'Неверные учетные данные.'}, HTTPStatus.UNAUTHORIZED
    result = get_tokens(request, login_user, db)
    return result
