from typing import Any
from dotenv import load_dotenv
from app.logger import logger
from os import getenv
from pathlib import Path


base_dir = Path(__file__).parent.parent


def get_path_env(key: str, default: Any, resolve: bool = False) -> Path:
    path_env = Path(getenv(key, default))

    if path_env.is_relative_to(base_dir):
        path_env = base_dir.joinpath(path_env)

    return path_env.resolve() if resolve else path_env


APP_DOTENV_PATH = get_path_env("APP_DOTENV_PATH", ".env.dev")
logger.info(f"App .env path: {APP_DOTENV_PATH}")

load_dotenv(APP_DOTENV_PATH)

ALLOWED_EXTENSIONS = {"csv"}
APP_SECRET = getenv("APP_SECRET", "JKLjk12pA@#12kjo0piu9012x")
APP_JWT_SECRET_KEY = getenv("APP_JWT_SECRET_KEY", "jkl@48uzgO#29XXJk123x")
APP_JWT_COOKIE_CSRF_PROTECT = bool(getenv("APP_JWT_COOKIE_CSRF_PROTECT", True))
APP_DEBUG = bool(getenv("APP_DEBUG", True))
APP_LISTEN_HOST = getenv("APP_LISTEN_HOST", "localhost")
APP_LISTEN_PORT = int(getenv("APP_LISTEN_PORT", 8000))
APP_DATABASE_PATH = get_path_env("APP_DATABASE_PATH", "db/database.sqlite")
APP_UPLOAD_FOLDER = get_path_env("APP_UPLOAD_FOLDER", "D:/data/uploads")
APP_ANALYZES_FOLDER = get_path_env("APP_ANALYZES_FOLDER", "D:/data/analyzes")
APP_VISUALIZATIONS_FOLDER = get_path_env(
    "APP_VISUALIZATIONS_FOLDER", "D:/data/visualizations"
)

logger.info(f"App debug: {APP_DEBUG}")
logger.info(f"App listen host: {APP_LISTEN_HOST}")
logger.info(f"App listen port: {APP_LISTEN_PORT}")
logger.info(f"App database path: {APP_DATABASE_PATH}")
logger.info(f"App upload folder: {APP_UPLOAD_FOLDER}")
logger.info(f"App analyzes folder: {APP_UPLOAD_FOLDER}")
logger.info(f"App visualizations folder: {APP_UPLOAD_FOLDER}")
