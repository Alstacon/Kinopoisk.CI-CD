import calendar
import datetime
from typing import Optional

import jwt

from project.config import BaseConfig

from flask_restx import abort

from project.services import UsersService
from project.tools.security import compare_passwords, generate_tokens_func


class AuthService:

    def __init__(self, users_service: UsersService):
        self.user_service = users_service

    def create_user(self, data):
        self.user_service.create_user(data)

    def generate_tokens(self, data, is_refresh=False):
        user = self.user_service.get_item(data.get("email"))

        if user is None:
            abort(404)

        if not is_refresh:
            if not compare_passwords(user.password, data.get("password")):
                abort(400)

        return generate_tokens_func(user)

    def approve_refresh_token(self, refresh_token):
        try:
            data = jwt.decode(jwt=refresh_token, key=BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
            return self.generate_tokens(data, is_refresh=True)
        except Exception as e:
            abort(404)
