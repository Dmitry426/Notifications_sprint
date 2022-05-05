import os

from app import app, ma, jwt
from flask import jsonify
from flask import request
from flask_app.api.v1.auth.base import create_tokens
from flask_app.db.postgresql import db
from flask_app.db.redis import redis_db
from flask_app.models.models import User
from flask_app.utils.rate_limit import rate_limit
from flask_app.utils.utils import redis_key
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_REFRESH_TOKEN_EXPIRES = os.getenv('JWT_REFRESH_TOKEN_EXPIRES')


@app.route('/refresh', methods=['POST'])
@rate_limit()
@jwt_required(refresh=True)
def refresh():
    """
        Обновление refresh токена
        ---
        tags:
          - Auth

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
    identity = get_jwt_identity()
    old_refresh_token = request.headers.get('Authorization')[7:]
    refresh_user = db.session.query(User).filter_by(id=identity).first()
    if not refresh_user:
        return {'message': f'Такого пользователя больше не существует.'}, HTTPStatus.UNAUTHORIZED
    user_agent = request.user_agent.string
    jti = redis_key(refresh_user.id, user_agent)
    token_in_redis = redis_db.get(jti)
    if token_in_redis == old_refresh_token:
        access_token, refresh_token = create_tokens(refresh_user)
        redis_db.add_token(key=jti, expire=JWT_REFRESH_TOKEN_EXPIRES, value=refresh_token)
        return {
            'message': f'Сделан refresh для {refresh_user.username}',
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
    return jsonify(msg='Refresh token невалиден'), HTTPStatus.UNPROCESSABLE_ENTITY
