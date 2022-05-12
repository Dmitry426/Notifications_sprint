from http import HTTPStatus

from app import ma
from flask import abort, jsonify, make_response
from marshmallow import fields

from flask_app.db.postgresql import db
from flask_app.models.models import User
from flask_app.schemas.role import RoleAddSchema


class UserCreateSchema(ma.SQLAlchemySchema):
    def validate_username(self, username_to_check, user_id=None):
        user = User.query.filter_by(username=username_to_check).first()
        if user and user_id != user.id:
            abort(
                make_response(
                    jsonify(
                        message="Такой пользователь уже существует. Попробуйте другое имя"
                    ),
                    HTTPStatus.CONFLICT,
                )
            )

    def validate_email(self, email_to_check, user_id=None):
        email = User.query.filter_by(email=email_to_check).first()
        if email and user_id != email.id:
            abort(
                make_response(
                    jsonify(message="Такой email уже используется. Попробуйте другой."),
                    HTTPStatus.CONFLICT,
                )
            )

    class Meta:
        fields = ("username", "email", "password")
        model = User
        load_instance = True
        sqla_session = db.session


class UserSchema(UserCreateSchema):

    roles = ma.Nested(RoleAddSchema, many=True)

    class Meta:
        fields = (
            "id",
            "username",
            "email",
            "status",
            "roles",
            "created",
            "last_changed",
        )
        model = User
        load_instance = True
        sqla_session = db.session


class UserUpdateSchema(UserCreateSchema):
    roles = fields.List(fields.String())

    class Meta:
        fields = ("username", "email", "status", "roles", "password")
        model = User
        load_instance = True
        sqla_session = db.session


user_update_schema = UserUpdateSchema()
user_create_schema = UserCreateSchema()
user_schema = UserSchema()
users_schema = UserSchema(many=True)
