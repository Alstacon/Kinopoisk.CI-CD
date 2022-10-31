from functools import wraps
from typing import Callable

import jwt
from flask import request
from flask_restx import abort
from project.config import BaseConfig
from project.models import User


def auth_required(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        token = request.headers['Authorization'].split('Bearer ')[-1]
        try:
            data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
            user = User(id=data.get("id"), email=data.get("email"), password=data.get("password"),
                        name=data.get("name"), surname=data.get("surname"), favorite_film=data.get("favorite_film"))
        except Exception as e:
            print('JWT Decode exception', e)
            abort(401)

        else:
            return func(*args, **kwargs, user=user)
    return wrapper

