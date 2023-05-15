from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from resources.settings import Settings

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def initialize_services(app: Flask):
    _load_config(app)
    _load_services(app)

def _load_config(app: Flask):
    app.config['JWT_SECRET_KEY'] = Settings.JWT_SECRET_KEY
    app.config['TRAP_HTTP_EXCEPTIONS']=True
    app.config['SQLALCHEMY_DATABASE_URI'] = Settings.DB_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def _load_services(app: Flask):
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)