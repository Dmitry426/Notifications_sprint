from app import app, ma
from flask import request, jsonify
from flask_app.db.postgresql import db
from flask_app.models.models import User, Role
from flask_app.schemas.role import RoleAddSchema
from flask_app.utils.utils import superuser_required
from flask_jwt_extended import jwt_required
from http import HTTPStatus


@app.route('/users/<user_id>/remove_role', methods=['PUT'])
@jwt_required()
@superuser_required
def user_root_remove_role(user_id):
    """
        Удалить роль у пользователя
        ---
        tags:
          - Users_Roles
        parameters:
        - name: 'user_id'
          in: 'path'
          description: 'Id юзера, которого необходимо выбрать.'
          required: true
          type: 'string'
        - in: 'body'
          name: 'body'
          description: 'Какую роль удалить?'
          required: 'true'
          schema:
            type: 'UserCreateSchema'
            schema:
              type: 'object'
              properties:
                title:
                  type: 'string'
            example: {
                'title':'authenticated user'
            }
        responses:
          200:
            description: роль удалена у пользователя
          403:
            description: Доступ запрещен.
          404:
            description: Пользователь не найден.
          409:
            description: У пользователя не было такой роли.
          422:
            description: Данные невалидны.
    """
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        schema = RoleAddSchema()
        if user:
            json_data = request.json
            if not json_data:
                return {'message': f'Данные не предоставлены.'}, HTTPStatus.NOT_FOUND
            try:
                remove_role = schema.load(json_data, session=db.session)
            except Exception:
                return {'message': f'Данные невалидны.'}, HTTPStatus.UNPROCESSABLE_ENTITY
            schema.role_not_exist(remove_role.title)

            for u in user.roles:
                if str(remove_role.title) == str(u):
                    del_role = db.session.query(Role).filter(Role.title == remove_role.title).first()
                    user.roles.remove(del_role)
                    db.session.commit()
                    return jsonify(msg=f'роль: {remove_role.title} удалена у пользователя {user.username}'), HTTPStatus.OK
            return jsonify(msg=f'У пользователя не было такой роли'), HTTPStatus.CONFLICT
        return {'message': f'Пользователь не найден.'}, HTTPStatus.NOT_FOUND
    except Exception:
        return {'message': f'Пользователь не найден.'}, HTTPStatus.NOT_FOUND
