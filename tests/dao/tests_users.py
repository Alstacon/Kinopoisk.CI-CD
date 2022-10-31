import pytest

from project.dao import UsersDAO
from project.models import User


class TestUsersDAO:

    @pytest.fixture
    def users_dao(self, db):
        return UsersDAO(db.session)

    @pytest.fixture
    def user_1(self, db):
        u = User(id=1, email="email", password="password")
        db.session.add(u)
        db.session.commit()
        return u

    @pytest.fixture()
    def user_2(self, db):
        u = User(id=2, email="liame", password="drowssap")
        db.session.add(u)
        db.session.commit()
        return u

    def test_get_user_by_id(self, users_dao, user_1):
        assert users_dao.get_by_id(user_1.id) == user_1

    def test_get_user_by_email(self, users_dao, user_1):
        assert users_dao.get_by_email(user_1.email) == user_1

    def test_get_all_users(self, users_dao, user_1, user_2):
        assert users_dao.get_all() == [user_1, user_2]

    def test_create_user(self, users_dao):
        user = {
            "email": "imail",
            "password": "parol"
        }
        new_user = users_dao.create(user)
        assert new_user.email == user.get("email")

    def test_update_user(self, user_1, users_dao):
        user_1["email"] = "EMAIL"
        users_dao.update(user_1)
        assert user_1.email != "email"

