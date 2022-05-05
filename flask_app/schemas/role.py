from app import ma
from flask_app.models.models import Role
from flask_app.db.postgresql import db
from flask import abort, make_response, jsonify
from http import HTTPStatus


class RoleCreateSchema(ma.SQLAlchemySchema):
    def role_exist(self, role_to_check):
        role = Role.query.filter_by(title=role_to_check).first()
        if role:
            abort(make_response(jsonify(message='Роль с таким наименованием уже существует. Попробуйте другое имя.'),
                                HTTPStatus.CONFLICT))

    def role_not_exist(self, role_to_check):
        role = Role.query.filter_by(title=role_to_check).first()
        if not role:
            abort(make_response(jsonify(message='Такой роли не существует. Укажите другую роль.'),
                                HTTPStatus.CONFLICT))

    class Meta:
        fields = ('title', 'description')
        model = Role
        load_instance = True
        sqla_session = db.session


class RoleSchema(RoleCreateSchema):
    class Meta:
        fields = ('id', 'title', 'description', 'created', 'last_changed')
        model = Role
        load_instance = True
        sqla_session = db.session


class RoleAddSchema(RoleCreateSchema):
    class Meta:
        fields = ('title',)
        model = Role
        load_instance = True
        sqla_session = db.session


role_add_schema = RoleAddSchema(many=True)
role_create_schema = RoleCreateSchema()
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
