from app import app, ma
from flask import request, jsonify
from flask_app.db.postgresql import db
from flask_app.models.models import User, Role
from flask_app.schemas.role import RoleAddSchema
from flask_app.utils.utils import superuser_required
from flask_jwt_extended import jwt_required
from http import HTTPStatus


@app.route("/users/<user_id>/add_role", methods=['POST'])
@jwt_required()
@superuser_required
def user_root_add_role(user_id):
    """
        Добавить пользователю роль
        ---
        tags:
          - Users_Roles
        parameters:
        - name: "user_id"
          in: "path"
          description: "Id юзера, которого необходимо выбрать."
          required: true
          type: "string"
        - in: "body"
          name: "body"
          description: "Какую роль добавить?"
          required: "true"
          schema:
            type: "UserCreateSchema"
            schema:
              type: "object"
              properties:
                title:
                  type: "string"
            example: {
                "title":"authenticated user"
            }
        responses:
          200:
            description: Пользователю добавлена роль
          403:
            description: Доступ запрещен.
          404:
            description: Пользователь не найден.
          409:
            description: Такая роль у пользователя уже есть.
          422:
            description: Данные невалидны.
    """
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        schema = RoleAddSchema()
        if user:
            json_data = request.json
            if not json_data:
                return {"message": f"Данные не предоставлены."}, HTTPStatus.NOT_FOUND
            try:
                add_role = schema.load(json_data, session=db.session)
            except Exception:
                return {"message": f"Данные невалидны."}, HTTPStatus.UNPROCESSABLE_ENTITY
            schema.role_not_exist(add_role.title)
            for u in user.roles:
                if str(add_role.title) == str(u):
                    return jsonify(msg=f'Такая роль у пользователя уже есть'), HTTPStatus.CONFLICT
            role = db.session.query(Role).filter_by(title=add_role.title).first()
            user.roles.append(role)
            db.session.commit()
            return jsonify(msg=f'Пользователю {user.username} добавлена роль: {add_role.title}'), HTTPStatus.OK
        return {"message": f"Пользователь не найден."}, HTTPStatus.NOT_FOUND
    except Exception:
        return {"message": f"Пользователь не найден."}, HTTPStatus.NOT_FOUND
