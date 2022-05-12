import os

from flask_app.db.postgresql import db
from flask_app.db.redis import redis_db
from flask_app.models.models import User, Role, AuthHistory
from flask_app.schemas.user import user_create_schema
from flask_app.utils.utils import redis_key
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token


JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_REFRESH_TOKEN_EXPIRES = os.getenv('JWT_REFRESH_TOKEN_EXPIRES')
REDIRECT_URL = os.getenv('REDIRECT_URL')


def generate_confirmation_token(user, email):
    additional_claims = {'email': f'{email}', 'redirect_url': REDIRECT_URL}
    confirm_token: str = create_access_token(identity=user, additional_claims=additional_claims)
    return confirm_token


def confirm_token(token):
    try:
        claims = decode_token(token)
        return claims
    except Exception:
        return False


def create_tokens(user):
    roles = []
    for role in user.roles:
        roles.append(role)
    roles_str = roles[0]
    if len(roles) > 1:
        roles_str = ', '.join(map(str, roles))
    additional_claims = {'roles': f'{roles_str}'}
    access_token: str = create_access_token(identity=user.id, additional_claims=additional_claims)
    refresh_token: str = create_refresh_token(identity=user.id)
    return [access_token, refresh_token]


def get_tokens(request, user, db):
    access_token, refresh_token = create_tokens(user)
    user_agent = request.user_agent.string
    ip_address = request.remote_addr
    browser = request.user_agent.browser
    check_platform = request.user_agent.platform
    platform = 'other'
    if check_platform:
        if 'windows' in check_platform.lower():
            platform = 'windows'
        elif 'linux' in check_platform.lower():
            platform = 'linux'

    history = AuthHistory(user_id=user.id,
                          ip_address=ip_address,
                          user_agent=user_agent,
                          platform=platform,
                          browser=browser
                          )
    db.session.add(history)
    user = db.session.query(User).filter_by(id=user.id).first()
    user.auth_history.append(history)
    db.session.add(user)
    db.session.commit()

    jti = redis_key(user.id, user_agent)
    redis_db.add_token(key=jti, expire=JWT_REFRESH_TOKEN_EXPIRES, value=refresh_token)

    return {
        'message': f'Вы залогинены как {user.username}',
        'access_token': access_token,
        'refresh_token': refresh_token,
    }


def get_token_social_data(login, email):
    check_user = db.session.query(User).filter_by(email=email).first()
    if not check_user:
        user_create_schema.validate_username(check_user.username)
        check_user = User(username=login,
                          email=email,
                          password='ckbirjv_ckj;ysq_gfhjkm'
                          )
        check_user.status = True
        check_user.roles.append(db.session.query(Role).filter_by(title='authenticated user').first())
        db.session.add(check_user)
        db.session.commit()
    from flask import request
    result = get_tokens(request, check_user, db)
    return result
