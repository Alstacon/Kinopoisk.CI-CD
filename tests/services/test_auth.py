from unittest.mock import patch, MagicMock

import pytest

from project.models import User
from project.services import AuthService, UsersService
from project.tools.security import generate_tokens_func



class TestAuthService:

    @pytest.fixture
    @patch('project.dao.UsersDAO')
    def users_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_by_email.return_value = User(id=1, email="email", password="password")
        dao.get_all.return_value = [
            User(id=1, email="email", password="password"),
            User(id=2, email="liame", password="drowssap")
        ]
        dao.create.return_value = User(id=2, email="liame", password="drowssap")
        dao.update.return_value = User(id=1, email="email", password="wordpass", name="imya", surname="familia")
        return dao

    @pytest.fixture()
    def users_service(self, users_dao_mock):
        return UsersService(dao=users_dao_mock, user_dao=users_dao_mock)

    @pytest.fixture
    def auth_service(self, users_service):
        return AuthService(users_service)

    @pytest.fixture
    def tokens(self, auth_service):
        user = User(id=1, email="email", password="password")
        tokens = generate_tokens_func(user)
        return tokens


    def test_generate_tokens(self, auth_service, users_service, tokens, user_with_pass):
        users_service.get_item = MagicMock(return_value = user_with_pass)
        data = {
            "id": 1,
            "email": "email",
            "password": "Password"
        }
        auth_service.generate_tokens(data, is_refresh=False)

        assert "access_token" in tokens
        assert "refresh_token" in tokens


    def test_approve_refresh_token(self, auth_service, tokens):
        new_tokens = auth_service.approve_refresh_token(tokens['refresh_token'])
        assert "access_token" in new_tokens
        assert "refresh_token" in new_tokens






