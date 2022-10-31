import json
from typing import Optional
from unittest.mock import MagicMock

import pytest

from project.container import user_service
from project.models import User
from project.tools.security import generate_tokens_func


class TestUsersView:

    @pytest.fixture
    def user_1(self, db, create_auth_user):
        user, token = create_auth_user(1, "email@mail.ru")
        db.session.add(user)
        db.session.commit()
        return user

    def test_user_page(self, client, token):
        user_service.get_item = MagicMock(return_value=User(id=1, email="email"))
        response = client.get('/user/', headers={'Authorization': token})

        assert response.status_code == 200

        response = client.get('/user/')

        assert response.status_code == 401

    def test_user_update(self, client, token):
        data = {"name": "name", "surname": "surname"}
        user_service.update = MagicMock(return_value=User(id=1, email="email", name="name", surname="surname"))
        response = client.patch('/user/', data=json.dumps(data),
                                headers={'Content-Type': 'application/json',
                                         'Authorization': token})
        assert response.status_code == 200

        response = client.patch('/user/')

        assert response.status_code == 401

    def test_update_password_page(self, client, token, user_with_pass):
        data = {"old_password": "password", "new_password": "pass"}
        user_service.get_by_id = MagicMock(return_value=user_with_pass)
        response = client.put('/user/password/', data=json.dumps(data),
                              headers={'Content-Type': 'application/json',
                                       'Authorization': token})

        assert response.status_code == 200
