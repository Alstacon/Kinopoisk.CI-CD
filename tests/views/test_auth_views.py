import json
from unittest.mock import MagicMock

import pytest

from project.container import auth_service
from project.models import User
from project.tools.security import generate_password_hash, generate_tokens_func


class TestAuthView:

    @pytest.fixture
    def refresh_token(self):
        token = generate_tokens_func(User(id=1, email="email", password="password"))
        return token["refresh_token"]

    def test_register_page(self, client, user_with_pass):
        data = {"email": "email@mail.ru", "password": "password"}
        auth_service.create_user = MagicMock(return_value=user_with_pass)
        response = client.post('/auth/register/', data=json.dumps(data),
                               headers={"Content-Type": "application/json"})

        assert response.status_code == 200

    def test_login_page(self, client):
        data = {"email": "email@mail.ru", "password": "password"}
        auth_service.generate_tokens = MagicMock(return_value={1: 1, 2: 2})
        response = client.post('/auth/login/', data=json.dumps(data),
                               headers={"Content-Type": "application/json"})

        assert response.status_code == 200

    def test_refresh_page(self, client, refresh_token):
        data = {"refresh_token": refresh_token}
        response = client.put('/auth/login/', data=json.dumps(data),
                              headers={"Content-Type": "application/json"})

        assert response.status_code == 200
