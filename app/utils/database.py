from app.config import APP_DATABASE_PATH
from app import db
import os


def recreate_database():
    print("Dropping database!")
    db.drop_all()

    print("Creating database!")
    db.create_all()


def drop_database():
    print("Dropping database!")
    db.drop_all()
    if os.path.exists(APP_DATABASE_PATH):
        print(f"Removing file: {APP_DATABASE_PATH}")
        os.remove(APP_DATABASE_PATH)


def create_database():
    if os.path.exists(APP_DATABASE_PATH):
        print(f"Database already exists at {os.path.abspath(APP_DATABASE_PATH)}")
        return

    print("Creating database!")
    db.create_all()
