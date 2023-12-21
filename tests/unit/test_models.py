from app.models import Roles, Users
from flask_sqlalchemy import SQLAlchemy


class TestUsers:
    def test_get_all(self, db: SQLAlchemy):
        users = db.session.execute(db.select(Users)).scalars().all()

        assert isinstance(users, list)
        assert len(users) == 2

    def test_get_by_id(self, db: SQLAlchemy):
        user: Users = db.session.execute(
            db.select(Users).filter_by(id=1)
        ).scalar_one_or_none()

        assert isinstance(user, Users)

    def test_create(self, db: SQLAlchemy):
        new_user = Users(
            first_name="Bob",
            second_name="Ross",
            username="bobross",
            active=True,
            email="bob.ross@gmail.com",
            phone="+123789123978",
            role=Roles.ADMIN,
        )
        new_user.password = "jkZJK#@kn1x23"
        db.session.add(new_user)
        db.session.commit()

        assert isinstance(new_user, Users)
        assert new_user.id == 3
        assert new_user.first_name == "Bob"
        assert new_user.second_name == "Ross"
        assert new_user.username == "bobross"
        assert new_user.active == True
        assert new_user.role == Roles.ADMIN

    def test_update(self, db: SQLAlchemy):
        existing_user: Users = db.session.execute(
            db.select(Users).filter_by(id=3)
        ).scalar_one_or_none()
        existing_user.username = "bob_ross"
        db.session.commit()

        assert isinstance(existing_user, Users)
        assert existing_user.id == 3
        assert existing_user.username == "bob_ross"

    def test_delete(self, db: SQLAlchemy):
        existing_user: Users = db.session.execute(
            db.select(Users).filter_by(id=3)
        ).scalar_one_or_none()

        db.session.delete(existing_user)
        db.session.commit()

        assert isinstance(existing_user, Users)
        assert existing_user.id == 3
        assert existing_user.username == "bob_ross"
