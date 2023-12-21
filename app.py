from app.config import APP_DEBUG, APP_LISTEN_HOST, APP_LISTEN_PORT
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(APP_LISTEN_HOST, APP_LISTEN_PORT, APP_DEBUG)
