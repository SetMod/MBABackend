from dotenv import load_dotenv
import logging
import sys
import os

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

base_format = logging.Formatter(
    fmt="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s"
)

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(base_format)

logger.addHandler(stream_handler)

APP_DOTENV_PATH = os.getenv("APP_DOTENV_PATH", ".env.dev")
load_dotenv(APP_DOTENV_PATH)

APP_SECRET = "JKLjk12pA@#12kjo0piu9012x"
APP_DATABASE_PATH = os.getenv("APP_DATABASE_PATH", "../db/database.db")

# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
UPLOAD_FOLDER = "D:/data"
ANALYZES_UPLOAD_FOLDER = "D:/data/analyzes"
VISUALIZATIONS_UPLOAD_FOLDER = "D:/data/visualizations"
ALLOWED_EXTENSIONS = {"csv"}

APP_LISTEN_HOST = os.getenv("APP_LISTEN_HOST", "localhost")
APP_LISTEN_PORT = int(os.getenv("APP_LISTEN_PORT", 8000))
APP_DEBUG = bool(os.getenv("APP_DEBUG", True))
