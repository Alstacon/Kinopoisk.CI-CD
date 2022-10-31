from typing import Optional

from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO
from project.models import Genre, Director, Movie, User, favorites


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def update(self, user: User):
        self._db_session.add(user)
        self._db_session.commit()

    def delete_from_favorites(self, movie_id: int, user_id: int) -> None| bool:
        if user := self.get_by_id(user_id):
            movie = self._db_session.query(Movie).get_or_404(movie_id)

            user.favorites.remove(movie)
            self._db_session.commit()
            return True
        return False

    def add_to_favorites(self, movie_id: int, user_id: int) -> None | bool:
        if user := self.get_by_id(user_id):
            movie = self._db_session.query(Movie).get_or_404(movie_id)

            user.favorites.append(movie)
            self._db_session.commit()
            return True
        return False

    def get_favorites(self, user_id: int, page: Optional[int] = None) -> list[Movie]:
        user = self.get_by_id(user_id)
        if page:
            try:
                return user.favorites(page, self._items_per_page).items
            except NotFound:
                return []
        return user.favorites
