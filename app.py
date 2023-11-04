from app import app
from app.config import APP_DEBUG, APP_LISTEN_HOST, APP_LISTEN_PORT

if __name__ == "__main__":
    app.run(APP_LISTEN_HOST, APP_LISTEN_PORT, APP_DEBUG)
