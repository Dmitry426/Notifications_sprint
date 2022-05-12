import functools
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity
from passlib.hash import argon2

from flask_app.models.models import User


def verify_password(user, password):
    return argon2.verify(password, user.hashed_password)


def hash_password(password):
    return argon2.hash(password)


def redis_key(user_id, user_agent):
    return f"{user_id}::{user_agent}"


def superuser_required(fn):
    @functools.wraps(fn)
    def decorator(*args, **kwargs):
        user_id = get_jwt_identity()
        current_user = User.query.get_or_404(user_id)
        role_data = [str(role) for role in current_user.roles]
        if "root" not in role_data:
            return {"message": f"ЗАПРЕЩЕНО."}, HTTPStatus.FORBIDDEN
        return fn(*args, **kwargs)

    return decorator
