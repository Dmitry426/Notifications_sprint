import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

DB_HOST: str = os.getenv('DB_HOST')
DB_NAME: str = os.getenv('DB_NAME')
DB_USER: str = os.getenv('DB_USER')
DB_PASSWORD: str = os.getenv('DB_PASSWORD')
DB_PORT: int = int(os.getenv('DB_PORT'))

db_url: str = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
SECRET_KEY = os.urandom(32)

db = SQLAlchemy()
migrate = Migrate()

engine = create_engine(db_url)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()


if not database_exists(engine.url):
    create_database(engine.url)


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['DEBUG'] = True

    db.init_app(app)

    with app.app_context():
        from flask_app.models.models import User, Role
        # from models.models import User, Role
        migrate.init_app(app, db)
        # db.create_all()
        # db.session.commit()
        if not Role.query.filter_by(title='root').first():
            user1 = Role(title='root', description='Суперпользователь')
            user1.save_to_db()
            Role(title='administrator', description='Роль для администратора.').save_to_db()
            Role(title='subscriber', description='Роль для просмотра скрытого контента.').save_to_db()
            Role(title='authenticated user', description='Роль для авторизованного пользователя.').save_to_db()
            Role(title='anonymous user', description='Роль для анонимного пользователя.').save_to_db()
        if not User.query.filter_by(username='admin').first():
            super_user = User(username='admin', email='menergo@mail.ru', password='123123', status=True)
            super_user.roles.append(Role.query.filter_by(title='root').first())
            super_user.save_to_db()

