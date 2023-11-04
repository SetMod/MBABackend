from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from app.config import APP_DATABASE_PATH, ALLOWED_EXTENSIONS, UPLOAD_FOLDER

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{APP_DATABASE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "s3crEt"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024 * 1024
CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)
