from app.config import APP_DATABASE_PATH
from app.db import db
from app import create_app
import argparse
import os


def recreate_database():
    db.drop_all()
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


if __name__ == "__main__":
    app = create_app()
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create-db", action="store_true")
    parser.add_argument("-d", "--delete-db", action="store_true")
    parser.add_argument("-r", "--recreate-db", action="store_true")
    args = parser.parse_args()

    if args.create_db:
        with app.app_context():
            create_database()
    elif args.delete_db:
        with app.app_context():
            drop_database()
    elif args.recreate_db:
        with app.app_context():
            recreate_database()
    else:
        parser.print_help()
