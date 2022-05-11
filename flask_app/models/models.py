import uuid

from enum import Enum
from flask import abort, make_response, jsonify
from http import HTTPStatus
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from db.postgresql import db


def create_partition(target, connection, **kw) -> None:
    """ creating partition by auth_history """
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_windows" PARTITION OF "auth_history" FOR VALUES IN ('windows')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_linux" PARTITION OF "auth_history" FOR VALUES IN ('linux')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_other" PARTITION OF "auth_history" FOR VALUES IN ('other')"""
    )


class DefaultRoleEnum(str, Enum):
    guest = 'anonymous user'
    user = 'authenticated user'
    subscriber = 'subscriber'
    administrator = 'administrator'
    root = 'root'


class TimestampMixin:
    created = db.Column(db.DateTime(timezone=True), default=db.func.now(), nullable=False)
    last_changed = db.Column(db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now(), nullable=False)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            abort(make_response(jsonify(message='Не удалось сделать commit в БД.'),
                                HTTPStatus.UNAUTHORIZED))


role_relationships = db.Table(
    'role_relationships',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False),
    db.Column('role_id', UUID(as_uuid=True), db.ForeignKey('role.id'), nullable=False)
)


class User(db.Model, TimestampMixin):
    __tablename__ = 'user'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(length=100), nullable=False, unique=True)
    email = db.Column(db.String(length=255), nullable=False, unique=True)
    password = db.Column(db.String(length=255), nullable=False)
    status = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=role_relationships, backref='user', lazy='dynamic')
    auth_history = db.relationship('AuthHistory', back_populates='user')

    def __repr__(self):
        return f'{self.username}'


class Role(db.Model, TimestampMixin):
    __tablename__ = 'role'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'{self.title}'

    class Meta:
        PROTECTED_ROLE_NAMES = (
            DefaultRoleEnum.guest.value,
            DefaultRoleEnum.user.value,
            DefaultRoleEnum.subscriber.value,
            DefaultRoleEnum.administrator.value,
            DefaultRoleEnum.root.value
        )


class AuthHistory(db.Model, TimestampMixin):
    __tablename__ = 'auth_history'
    __table_args__ = (
        UniqueConstraint('id', 'platform'),
        {
            'postgresql_partition_by': 'LIST (platform)',
            'listeners': [('after_create', create_partition)],
        }
    )
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='auth_history')
    ip_address = db.Column(db.String(100))
    user_agent = db.Column(db.Text, nullable=False)
    platform = db.Column(db.Text)
    browser = db.Column(db.Text)
