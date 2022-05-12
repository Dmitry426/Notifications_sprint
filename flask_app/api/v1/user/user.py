from http import HTTPStatus

from app import app, ma
from flask import request
from flask_jwt_extended import jwt_required

from flask_app.db.postgresql import db
from flask_app.models.models import User
from flask_app.schemas.user import user_create_schema, user_schema
from flask_app.utils.utils import superuser_required


@app.route("/users/<user_id>", methods=["GET"])
@jwt_required()
@superuser_required
def user_root_detail(user_id):
    """
    Информация о пользователе
    ---
    tags:
      - SuperUser
    parameters:
    - name: 'user_id'
      in: 'path'
      description: 'Id Пользователя, которого необходимо выбрать.'
      required: true
      type: 'string'
    responses:
      200:
        description: Информация о пользователе
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
        description: Пользователь не найден

    """
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        schema_view = user_schema
        if user:
            return schema_view.dump(user), HTTPStatus.OK
        return {"message": f"Пользователь не найден."}, HTTPStatus.NOT_FOUND
    except Exception:
        return {"message": f"Пользователь не найден."}, HTTPStatus.NOT_FOUND


@app.route("/users/<user_id>", methods=["PUT"])
@jwt_required()
@superuser_required
def user_root_put_detail(user_id):
    """
    Обновление данных пользователя
    ---
    tags:
      - SuperUser
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
    """
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        schema_view = user_schema
        schema_make = user_create_schema
        if user:
            json_data = request.json
            if not json_data:
                return {"message": f"Данные не предоставлены."}, HTTPStatus.NOT_FOUND
            try:
                user_edit = schema_make.load(json_data, session=db.session)
            except Exception:
                return {
                    "message": f"Данные невалидны."
                }, HTTPStatus.UNPROCESSABLE_ENTITY
            schema_make.validate_email(user_edit.email, user.id)
            schema_make.validate_username(user_edit.username, user.id)
            user.password = user_edit.password
            user.username = user_edit.username
            user.email = user_edit.email
            db.session.add(user)
            db.session.commit()
            return schema_view.dump(user), HTTPStatus.OK
        return {"message": f"Пользователь не найден."}, HTTPStatus.NOT_FOUND
    except Exception:
        return {"message": f"Пользователь не найден."}, HTTPStatus.NOT_FOUND


@app.route("/users/<user_id>", methods=["DELETE"])
@jwt_required()
@superuser_required
def root_delete_user(user_id):
    """
    Удаление пользователя
    ---
    tags:
      - SuperUser
    parameters:
    - name: 'user_id'
      in: 'path'
      description: 'Id Пользователя, которого необходимо выбрать.'
      required: true
      type: 'string'
    responses:
      204:
        description: Учетная запись была удалена.
      400:
        description: Этого пользователя удалить невозможно.
      403:
        description: Доступ запрещен.
      404:
        description: Пользователь не найден.
    """
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        if user:
            deleted_user = user.username
            db.session.delete(user)
            db.session.commit()
            return f"Учетная запись {deleted_user} была удалена.", HTTPStatus.NO_CONTENT
        return {"message": f"Пользователь не найден."}, HTTPStatus.NOT_FOUND
    except Exception:
        return {"message": f"Пользователь не найден."}, HTTPStatus.NOT_FOUND
