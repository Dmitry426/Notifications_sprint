from http import HTTPStatus

from app import app
from flask_jwt_extended import jwt_required

from flask_app.models.models import User
from flask_app.schemas.user import users_schema
from flask_app.utils.utils import superuser_required


@app.route("/users")
@jwt_required()
@superuser_required
def users_list():
    """
    Список пользователя
    ---
    tags:
      - Users
    responses:
      200:
        description: Список пользователя
        type: 'array'
        items:
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
        description: Пользователи еще не созданы.
    """
    users = User.query.all()
    if users:
        return {"users": users_schema.dump(users)}, HTTPStatus.OK
    return {"message": f"Пользователи еще не созданы."}, HTTPStatus.NOT_FOUND
