import base64
import hashlib

import pytest

from project.models import User
from project.tools.security import generate_password_hash, generate_tokens_func, compare_passwords


class TestTools:

    @pytest.fixture
    def old_hash(self):
        password = "password"
        new_hash = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=base64.b64decode("salt"),
            iterations=100_000,
        )
        return base64.b64encode(new_hash).decode('utf-8')


    @pytest.mark.parametrize('user', [User(id=1, email='email', password='password')])
    def test_generate_tokens_func(self, user):
        tokens = generate_tokens_func(user)
        assert 'access_token' in tokens
        assert 'refresh_token' in tokens
        assert tokens['access_token'] != tokens['refresh_token']

    @pytest.mark.parametrize('password', ['password'], )
    def test_compare_passwords(self, old_hash, password):
        assert compare_passwords(old_hash, password)


    @pytest.mark.parametrize('password', ['password'])
    def test_generate_password_hash(self, password, app):
        assert generate_password_hash(password)

