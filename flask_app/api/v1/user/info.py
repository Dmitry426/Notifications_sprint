from app import app, ma
from flask import request
from flask_app.db.postgresql import db
from flask_app.models.models import User
from flask_app.schemas.user import user_schema, user_create_schema
from flask_app.utils.rate_limit import rate_limit
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus


@app.route('/users/<user_id>/info', methods=['GET'])
@rate_limit()
@jwt_required()
def user_detail(user_id):
    """
        Просмотр информации пользователя
        ---
        tags:
          - Users
        parameters:
          - name: 'user_id'
            in: 'path'
            description: 'ID юзера, которого необходимо выбрать.'
            required: true
            type: 'string'
        responses:
          200:
            description: Просмотр информации пользователя
            schema:
              type: 'object'
              properties:
                created:
                  type: 'string'
                  format: 'date-time'
                email:
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
            description: Пользователь не найден.
          422:
            description: Данные невалидны.
          429:
            description: Слишком много запросов с одного ip-адреса. Limit limit in interval seconds.
    """
    identity = get_jwt_identity()
    if user_id != identity:
        return {'message': f'ЗАПРЕЩЕНО.'}, HTTPStatus.FORBIDDEN
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        schema_view = user_schema
        if user:
            return schema_view.dump(user), HTTPStatus.OK
        return {'message': f'Пользователь не найден.'}, HTTPStatus.NOT_FOUND
    except Exception:
        return {'message': f'Пользователь не найден.'}, HTTPStatus.NOT_FOUND


@app.route('/users/<user_id>/info', methods=['PUT'])
@rate_limit()
@jwt_required()
def user_update_detail(user_id):
    """
        Обновление данных пользователя
        ---
        tags:
          - Users
        parameters:
        - name: 'user_id'
          in: 'path'
          description: 'Id юзера, которого необходимо выбрать.'
          required: true
          type: 'string'
        - in: 'body'
          name: 'body'
          description: 'Можно изменить логин, электронную почту и пароль'
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
                'username':'t4444ester',
                'email': 'mai4444ld09@mail.ru',
                'password': '123123'
            }
        responses:
          200:
            description: Данные пользователя обновлены
            schema:
              type: 'object'
              properties:
                created:
                  type: 'string'
                  format: 'date-time'
                email:
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
          403:
            description: Доступ запрещен.
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
    identity = get_jwt_identity()
    if user_id != identity:
        return {'message': f'ЗАПРЕЩЕНО.'}, HTTPStatus.FORBIDDEN
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        schema_view = user_schema
        schema_make = user_create_schema
        if user:
            json_data = request.json
            if not json_data:
                return {'message': f'Данные не предоставлены.'}, HTTPStatus.NOT_FOUND
            try:
                user_edit = schema_make.load(json_data, session=db.session)
            except ma.ValidationError:
                return {'message': f'Данные невалидны.'}, HTTPStatus.UNPROCESSABLE_ENTITY
            schema_make.validate_username(user_edit.username, user.id)
            schema_make.validate_email(user_edit.email, user.id)

            user.username = user_edit.username
            user.email = user_edit.email
            user.password = user_edit.password

            db.session.add(user)
            db.session.commit()
            return schema_view.dump(user), HTTPStatus.OK
        return {'message': f'Пользователь не найден.'}, HTTPStatus.NOT_FOUND
    except Exception:
        return {'message': f'Пользователь не найден.'}, HTTPStatus.NOT_FOUND
