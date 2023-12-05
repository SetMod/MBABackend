from flask import Flask
from app.config import APP_DATABASE_PATH
from app.db import db
from app import create_app
from app.models import OrganizationMembers, OrganizationRoles, Organizations, Users, Roles
import argparse
import os


def recreate_database(app: Flask):
    drop_database(app)
    create_database(app)


def drop_database(app: Flask):
    print("Dropping database!")

    with app.app_context():
        db.drop_all()

    if os.path.exists(APP_DATABASE_PATH):
        print(f"Removing file: {APP_DATABASE_PATH}")
        os.remove(APP_DATABASE_PATH)


def create_database(app: Flask):
    if os.path.exists(APP_DATABASE_PATH):
        print(f"Database already exists at {os.path.abspath(APP_DATABASE_PATH)}")
        return

    print("Creating database!")
    with app.app_context():
        db.create_all()

        user = Users()
        user.username = "guest"
        user.password = "guest"
        user.first_name = "First"
        user.second_name = "Guest"
        user.email = "guest@example.com"
        user.phone = "+123456567123"
        user.active = True
        user.role = Roles.ADMIN

        org1 = Organizations()
        org1.name = "LocalStore"
        org1.description = "LocalStore organization for local stores"
        org1.email = "business@localstore.com"
        org1.phone = "+123123123123"

        member1 = OrganizationMembers()
        member1.user_id = 1
        member1.organization_id = 1
        member1.active = True
        member1.role = OrganizationRoles.OWNER

        db.session.add(user)
        db.session.add(org1)
        db.session.add(member1)
        db.session.commit()


if __name__ == "__main__":
    app = create_app()
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create-db", action="store_true")
    parser.add_argument("-d", "--delete-db", action="store_true")
    parser.add_argument("-r", "--recreate-db", action="store_true")
    args = parser.parse_args()

    if args.create_db:
        create_database(app)
    elif args.delete_db:
        drop_database(app)
    elif args.recreate_db:
        recreate_database(app)
    else:
        parser.print_help()
