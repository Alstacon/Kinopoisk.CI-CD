from typing import Generic, List, Optional, TypeVar

from flask import current_app
from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound

from project.exceptions import CondlictError
from project.setup.db.models import Base

T = TypeVar('T', bound=Base)


class BaseDAO(Generic[T]):
    __model__ = Base

    def __init__(self, db_session: scoped_session) -> None:
        self._db_session = db_session

    @property
    def _items_per_page(self) -> int:
        return current_app.config['ITEMS_PER_PAGE']

    def get_by_id(self, pk: int) -> Optional[T]:
        return self._db_session.query(self.__model__).get(pk)

    def get_by_email(self, email: str):
        return self._db_session.query(self.__model__).filter(self.__model__.email == email).first()

    def get_by_user_id(self, user_id):
        return self._db_session.query(self.__model__).filter(self.__model__.user_id == user_id).all()


    def get_all(self, page: Optional[int] = None) -> List[T]:
        stmt: BaseQuery = self._db_session.query(self.__model__)
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

    def get_all_sorted_by_year(self, page: Optional[int] = None) -> List[T]:
        stmt: BaseQuery = self._db_session.query(self.__model__)
        stmt = stmt.order_by(desc(self.__model__.year))
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

    def create(self, data):
        try:
            entity = self.__model__(**data)
            self._db_session.add(entity)
            self._db_session.commit()
            return entity
        except Exception:
            raise CondlictError(f"""User with email {data.get("email")} is already registered""")




