from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os

# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
UPLOAD_FOLDER = 'D:\\data'
ANALYZES_UPLOAD_FOLDER = 'D:\\data\\analyzes'
VISUALIZATIONS_UPLOAD_FOLDER = 'D:\\data\\visualizations'
ALLOWED_EXTENSIONS = {'csv'}
os.environ['FLASK_APP'] = 'app'
os.environ['FLASK_ENV'] = 'development'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "s3crEt"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024
CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)
