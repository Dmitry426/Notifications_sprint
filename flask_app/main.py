import view
from app import app

import flask_app.api.v1.auth.login
import flask_app.api.v1.auth.logout
import flask_app.api.v1.auth.oauth
import flask_app.api.v1.auth.refresh
import flask_app.api.v1.role.add
import flask_app.api.v1.role.role
import flask_app.api.v1.role.roles
import flask_app.api.v1.user.add
import flask_app.api.v1.user.add_role
import flask_app.api.v1.user.confirm
import flask_app.api.v1.user.history
import flask_app.api.v1.user.info
import flask_app.api.v1.user.remove_role
import flask_app.api.v1.user.user
import flask_app.api.v1.user.users

if __name__ == "__main__":
    app.run()
