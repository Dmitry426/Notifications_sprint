from app import app, ma
from flask import request
from flask_app.schemas.role import RoleSchema
from flask_app.db.postgresql import db
from flask_jwt_extended import jwt_required
from flask_app.utils.utils import superuser_required
from http import HTTPStatus


@app.route('/roles/add', methods=['POST'])
@jwt_required()
@superuser_required
def role_add():
    """
        Создание роли
        ---
        tags:
          - Roles
        parameters:
        - in: 'body'
          name: 'body'
          description: 'Укажите наименование роли и дайте её описание'
          required: 'true'
          schema:
            type: 'UserCreateSchema'
            schema:
              type: 'object'
              properties:
                title:
                  type: 'string'
                description:
                  type: 'string'
            example: {
                'title':'userr5le4244',
                'description': 'Роль для удаления.'
            }
        responses:
          201:
            description: Роль создана
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
          404:
            description: Данные не предоставлены.
          409:
            description: Такая роль уже существует.
          422:
            description: Данные невалидны.
    """
    schema = RoleSchema()
    json_data = request.json
    if not json_data:
        return {'message': f'Данные не предоставлены.'}, HTTPStatus.NOT_FOUND
    try:
        new_role = schema.load(json_data, session=db.session)
    except ma.ValidationError:
        return {'message': f'Данные невалидны.'}, HTTPStatus.UNPROCESSABLE_ENTITY
    schema.role_exist(new_role.title)
    db.session.add(new_role)
    db.session.commit()
    return schema.dump(new_role), HTTPStatus.CREATED
