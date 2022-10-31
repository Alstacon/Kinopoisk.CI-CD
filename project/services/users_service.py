from typing import Optional

from project.tools.security import compare_passwords
from project.dao.base import BaseDAO
from project.dao.main import UsersDAO
from project.exceptions import ItemNotFound
from project.models import User
from project.tools.security import generate_password_hash


class UsersService:
    def __init__(self, dao: BaseDAO, user_dao: UsersDAO) -> None:
        self.dao = dao
        self.user_dao = user_dao

    def get_by_id(self, user_id: int):
        user = self.dao.get_by_id(user_id)
        return user

    def get_item(self, email: str) -> User:
        if user := self.dao.get_by_email(email):
            return user
        raise ItemNotFound(f'User with email={email} not exists.')

    def create_user(self, data):
        data['password'] = generate_password_hash(data.get('password'))
        return self.dao.create(data)

    def add_to_favorites(self, movie_id, user_id):
        return self.user_dao.add_to_favorites(movie_id, user_id)

    def delete_from_favorites(self, movie_id, user_id):
        return self.user_dao.delete_from_favorites(movie_id, user_id)

    def get_favorites(self, user_id):
        return self.user_dao.get_favorites(user_id)


    def update(self, user, data: dict):
        user = self.user_dao.get_by_email(user.email)
        if 'name' in data:
            user.name = data.get('name')
        if 'surname' in data:
            user.surname = data.get('surname')
        if 'favorite_movies' in data:
            user.favorite_movies = data.get('favorite_movies')
        return self.user_dao.update(user)

    def update_password(self, user, old_password, new_password):
        user = self.get_by_id(user.id)
        if compare_passwords(user.password, old_password):
            user.password = generate_password_hash(new_password)
            return self.user_dao.update(user)
        return "Неверный пароль"



