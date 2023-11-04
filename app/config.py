from dotenv import load_dotenv
import os

APP_DOTENV_PATH = os.getenv("APP_DOTENV_PATH", ".env.dev")

load_dotenv(APP_DOTENV_PATH)

print(os.getenv("FLASK_APP"))
print(os.getenv("FLASK_ENV"))

APP_DATABASE_PATH = os.getenv("APP_DATABASE_PATH", "../db/database.db")

# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
UPLOAD_FOLDER = "D:/data"
ANALYZES_UPLOAD_FOLDER = "D:/data/analyzes"
VISUALIZATIONS_UPLOAD_FOLDER = "D:/data/visualizations"
ALLOWED_EXTENSIONS = {"csv"}

APP_LISTEN_HOST = os.getenv("APP_LISTEN_HOST", "localhost")
APP_LISTEN_PORT = int(os.getenv("APP_LISTEN_PORT", 8000))
APP_DEBUG = bool(os.getenv("APP_DEBUG", True))
