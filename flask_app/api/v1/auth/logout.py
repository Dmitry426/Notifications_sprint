import os

from app import app, ma, jwt
from flask import request
from flask_app.db.postgresql import db
from flask_app.models.models import User
from flask_app.db.redis import redis_db
from flask_app.utils.utils import redis_key
from flask_app.utils.rate_limit import rate_limit
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from http import HTTPStatus

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_REFRESH_TOKEN_EXPIRES = os.getenv('JWT_REFRESH_TOKEN_EXPIRES')
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))


@app.route('/logout', methods=['DELETE'])
@rate_limit()
@jwt_required()
def logout():
    """
        Разлогиневание пользователя
        ---
        tags:
          - Auth
        responses:
          200:
            description: Вы разлогинены
          401:
            description: Такого пользователя больше не существует.
          429:
            description: Слишком много запросов с одного ip-адреса. Limit limit in interval seconds.
        """

    identity = get_jwt_identity()
    logout_user = db.session.query(User).filter_by(id=identity).first()
    if not logout_user:
        return {'message': f'Такого пользователя больше не существует.'}, HTTPStatus.UNAUTHORIZED
    user_agent = request.user_agent.string
    jti = redis_key(logout_user.id, user_agent)
    redis_db.delete_token(jti)

    jti = get_jwt()['jti']
    redis_db.set(jti, '', ex=3600)

    return {'message': f'Вы разлогинены.'}, HTTPStatus.OK
