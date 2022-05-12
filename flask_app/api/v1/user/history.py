from app import app, ma
from flask import jsonify, request
from flask_app.models.models import User, AuthHistory
from flask_app.schemas.history import histories_schema
from flask_app.db.postgresql import db
from flask_app.utils.rate_limit import rate_limit
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus


@app.route('/users/<user_id>/history')
@rate_limit()
@jwt_required()
def user_history(user_id):
    """
        История авторизаций пользователя
        ---
        tags:
          - Users
        parameters:
          - name: 'user_id'
            in: 'path'
            description: 'Id юзера, которого необходимо выбрать.'
            required: true
            type: 'string'
          - name: 'page'
            in: 'query'
            description: 'Номер страницы'
            required: true
            type: 'string'
          - name: 'per_page'
            in: 'query'
            description: 'Количество элементов на странице'
            required: true
            type: 'string'
        responses:
          200:
            description: История авторизаций пользователя
            schema:
              type: 'object'
              properties:
                created:
                  type: 'string'
                  format: 'date-time'
                browser:
                  type: 'string'
                ip_address:
                  type: 'string'
                platform:
                  type: 'string'
                user_agent:
                  type: 'string'
          401:
            description: Несанкционированный доступ.
          403:
            description: Доступ запрещен.
          404:
            description: Пользователь не найден.
          429:
            description: Слишком много запросов с одного ip-адреса. Limit limit in interval seconds.
        """
    identity = get_jwt_identity()
    if user_id != identity:
        return {'message': f'ЗАПРЕЩЕНО.'}, HTTPStatus.FORBIDDEN
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        if user:
            page = int(request.args.get('page'))
            per_page = int(request.args.get('per_page'))
            if page <= 0:
                raise AttributeError('page needs to be >= 1')
            if per_page <= 0:
                raise AttributeError('page_size needs to be >= 1')
            items = db.session.query(AuthHistory).filter_by(
                user_id=user.id).limit(per_page).offset((page - 1) * per_page).all()
            history = histories_schema.dump(items)
            return jsonify(history), HTTPStatus.OK
        return {'message': f'Пользователь не найден.'}, HTTPStatus.NOT_FOUND
    except Exception:
        return {'message': f'Пользователь не найден.'}, HTTPStatus.NOT_FOUND
