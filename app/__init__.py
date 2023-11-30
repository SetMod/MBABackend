from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from app.logger import logger
from app.config import (
    APP_DATABASE_PATH,
    ALLOWED_EXTENSIONS,
    APP_UPLOAD_FOLDER,
    APP_SECRET,
    APP_JWT_SECRET_KEY,
    APP_JWT_COOKIE_CSRF_PROTECT,
)
from sqlalchemy.exc import OperationalError
from app.db import db, ma, migrate
from app.jwt import jwt
from app.mail import mail
from app.routes import register_blueprints


def create_database(app: Flask, db: SQLAlchemy):
    if APP_DATABASE_PATH.exists():
        logger.info(f"Database already exists at {APP_DATABASE_PATH}")
        return

    with app.app_context():
        logger.info(f"Creating database at {APP_DATABASE_PATH}")
        try:
            db.create_all()
        except OperationalError as err:
            logger.error(
                f"Failed to create database at {APP_DATABASE_PATH}. Message: {err.orig}"
            )
            logger.exception(err)
            exit(1)
        except Exception as err:
            logger.error(
                f"Failed to create database at {APP_DATABASE_PATH}. Message: {err}"
            )
            logger.exception(err)
            exit(1)


def create_app() -> Flask:
    app = Flask(__name__)
    app.instance_path = "db"
    app.secret_key = APP_SECRET
    app.static_folder = None
    app.logger = logger

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{APP_DATABASE_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["APP_UPLOAD_FOLDER"] = APP_UPLOAD_FOLDER
    app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024 * 1024
    app.config["JWT_SECRET_KEY"] = APP_JWT_SECRET_KEY
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = APP_JWT_COOKIE_CSRF_PROTECT
    CORS(app)

    jwt.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    migrate.init_app(app)

    create_database(app, db)
    register_blueprints(app)

    return app
