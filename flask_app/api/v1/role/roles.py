from app import app
from flask_app.models.models import Role
from flask_app.schemas.role import roles_schema
from flask_jwt_extended import jwt_required
from flask_app.utils.utils import superuser_required
from http import HTTPStatus


@app.route('/roles')
@jwt_required()
@superuser_required
def roles_list():
    """
        Список ролей
        ---
        tags:
          - Roles
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
                id:
                  type: 'string'
                  format: 'uuid'
                description:
                  type: 'string'
                last_changed:
                  type: 'string'
                  format: 'date-time'
                title:
                  type: 'string'
          403:
            description: Доступ запрещен.
          404:
            description: Роли почему-то еще не созданы.
    """
    roles = Role.query.all()
    if roles:
        return {'roles': roles_schema.dump(roles)}
    return {'message': f'Роли почему-то еще не созданы.'}, HTTPStatus.NOT_FOUND
