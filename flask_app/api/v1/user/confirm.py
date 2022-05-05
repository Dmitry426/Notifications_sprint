from app import app, ma
from flask import redirect
from flask_app.api.v1.auth.base import confirm_token
from flask_app.db.postgresql import db
from flask_app.models.models import User
from flask_app.utils.rate_limit import rate_limit
from http import HTTPStatus


@app.route('/confirm/<token>', methods=['GET'])
@rate_limit()
def confirm_email(token):
    """
        Подтверждение Email нового пользователя
        ---
        tags:
          - Auth
        parameters:
          - name: 'Token'
            in: 'path'
            description: 'Введите токен для подтверждения Email'
            required: true
            type: 'string'
        responses:
          302:
            description: Пользователь подтвердил свой Email
          404:
            description: Ссылка просрочена.
          429:
            description: Слишком много запросов с одного ip-адреса. Limit limit in interval seconds.
    """
    claims = confirm_token(token)
    if claims:
        user_id = claims['sub']
        redirect_url = claims['redirect_url']
        user = db.session.query(User).filter_by(id=user_id).first()
        user.status = True
        db.session.add(user)
        db.session.commit()
        return redirect(redirect_url, code=HTTPStatus.FOUND)
    return {'message': f'Скорее всего ссылка недействительна.'}, HTTPStatus.NOT_FOUND
