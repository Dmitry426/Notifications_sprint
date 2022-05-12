from http import HTTPStatus

from app import app, ma
from flask import request
from flask_jwt_extended import jwt_required
from werkzeug import exceptions

from flask_app.db.postgresql import db
from flask_app.models.models import Role
from flask_app.schemas.role import role_create_schema, role_schema
from flask_app.utils.utils import superuser_required


@app.route("/roles/<role_id>", methods=["GET"])
@jwt_required()
@superuser_required
def role_detail(role_id):
    """
    Подробнее о роли
    ---
    tags:
      - Roles
    parameters:
    - name: 'role_id'
      in: 'path'
      description: 'ID роли, которую необходимо выбрать.'
      required: true
      type: 'string'
    responses:
      200:
        description: Подробнее о роли
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
        description: Роль не найдена.
      422:
        description: Данные невалидны.
    """
    try:
        role = db.session.query(Role).filter_by(id=role_id).first()
        schema_view = role_schema
        if role:
            return schema_view.dump(role), HTTPStatus.OK
        return {"message": f"Роль не найдена."}, HTTPStatus.NOT_FOUND
    except Exception:
        return {"message": f"Роль не найдена."}, HTTPStatus.NOT_FOUND


@app.route("/roles/<role_id>", methods=["PUT"])
@jwt_required()
@superuser_required
def role_put_detail(role_id):
    """
    Изменить данные в роли
    ---
    tags:
      - Roles
    parameters:
    - name: 'role_id'
      in: 'path'
      description: 'Id роли, которую необходимо выбрать.'
      required: true
      type: 'string'
    - in: 'body'
      name: 'body'
      description: 'Измените наименование роли или её описание'
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
            'title':'user_to_delete',
            'description': 'Роль для удаления.'
        }
    responses:
      200:
        description: Роль изменена
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
      400:
        description: Наименование этой роли изменить невозможно.
      404:
        description: Данные не предоставлены.
      409:
        description: Такая роль уже существует.
      422:
        description: Данные невалидны.
    """
    try:
        role = db.session.query(Role).filter_by(id=role_id).first()
        schema_view = role_schema
        schema_make = role_create_schema
        if role:
            json_data = request.json
            if not json_data:
                return {"message": f"Данные не предоставлены."}, HTTPStatus.NOT_FOUND
            try:
                role_edit = schema_make.load(json_data, session=db.session)
            except Exception:
                return {
                    "message": f"Данные невалидны."
                }, HTTPStatus.UNPROCESSABLE_ENTITY

            if role.title != role_edit.title:
                schema_make.role_exist(role_edit.title)
                if role.title in Role.Meta.PROTECTED_ROLE_NAMES:
                    raise exceptions.BadRequest(
                        "Наименование этой роли изменить невозможно."
                    )
            role.title = role_edit.title
            role.description = role_edit.description

            db.session.add(role)
            db.session.commit()
            return schema_view.dump(role), HTTPStatus.OK
        return {"message": f"Роль не найдена."}, HTTPStatus.NOT_FOUND
    except Exception:
        return {"message": f"Роль не найдена."}, HTTPStatus.NOT_FOUND


@app.route("/roles/<role_id>", methods=["DELETE"])
@jwt_required()
@superuser_required
def role_delete(role_id):
    """
    Удаление роли
    ---
    tags:
      - Roles
    parameters:
    - name: 'role_id'
      in: 'path'
      description: 'Id роли, которую необходимо выбрать.'
      required: true
      type: 'string'
    responses:
      204:
        description: Роль удалена
      400:
        description: Эту роль удалить невозможно.
      404:
        description: Данные не предоставлены.
      409:
        description: Такая роль уже существует.
      422:
        description: Данные невалидны.
    """
    try:
        role = db.session.query(Role).filter_by(id=role_id).first()
        if role:
            if role.title in Role.Meta.PROTECTED_ROLE_NAMES:
                raise exceptions.BadRequest("Эту роль удалить невозможно.")
            deleted_role = role.title
            db.session.delete(role)
            db.session.commit()
            return f"Роль {deleted_role} удалена.", HTTPStatus.NO_CONTENT
        return {"message": f"Роль не найдена."}, HTTPStatus.NOT_FOUND
    except Exception:
        return {"message": f"Роль не найдена."}, HTTPStatus.NOT_FOUND
