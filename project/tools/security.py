import base64
import calendar
import datetime
import hashlib
import hmac

import jwt
from flask import current_app

from project.config import BaseConfig


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compare_passwords(hash_password, password) -> bool:
    """compares the old hash from bd with the new one made from income password"""
    decoded_hash = base64.b64decode(hash_password)
    hash_digest = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        BaseConfig.PWD_HASH_SALT,
        BaseConfig.PWD_HASH_ITERATIONS
    )
    return hmac.compare_digest(decoded_hash, hash_digest)

def generate_tokens_func(user):
    data = {
        "id": user.id,
        "email": user.email,
        "password": user.password,
        "name": user.name,
        "surname": user.surname,
        "favorite_film": user.favorite_film
    }

    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data['exp'] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=BaseConfig.ALGORITHM)

    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data['exp'] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=BaseConfig.ALGORITHM)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }