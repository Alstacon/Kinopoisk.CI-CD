import pytest

from project.dao import MoviesDAO
from project.models import Movie


class TestMoviesDAO:

    @pytest.fixture
    def movies_dao(self, db):
        return MoviesDAO(db.session)

    @pytest.fixture
    def movie_1(self, db):
        m = Movie(title="Ночные звери", description="Desc",
                  trailer="link",
                  year=2016,
                  rating=5.0,
                  genre_id=1,
                  director_id=2
                  )
        db.session.add(m)
        db.session.commit()
        return m

    @pytest.fixture
    def movie_2(self, db):
        m = Movie(title="Исчезнувшая",
                  description="Desc",
                  trailer="link",
                  year=2017,
                  rating=5.0,
                  genre_id=1,
                  director_id=2
                  )
        db.session.add(m)
        db.session.commit()
        return m

    @pytest.fixture
    def movie_3(self, db):
        m = Movie(title="Элизабеттаун",
                  description="Desc",
                  trailer="link",
                  year=2005,
                  rating=5.0,
                  genre_id=1,
                  director_id=2
                  )
        db.session.add(m)
        db.session.commit()
        return m

    def test_get_movie_by_id(self, movie_1, movies_dao):
        assert movies_dao.get_by_id(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self, movies_dao):
        assert not movies_dao.get_by_id(1)

    def test_get_all_movies(self, movie_1, movie_2, movies_dao):
        assert movies_dao.get_all() == [movie_1, movie_2]

    def test_get_all_movies_sorted_by_year(self, app, movies_dao, movie_1, movie_2, movie_3):
        app.config["ITEMS_PER_PAGE"] = 2
        assert movies_dao.get_all_sorted_by_year(page=1) == [movie_2, movie_1]
        assert movies_dao.get_all_sorted_by_year(page=2) == [movie_3]
        assert movies_dao.get_all_sorted_by_year(page=3) == []

    def test_movie_create(self, movies_dao):
        movie = {"id": 4,
                 "title": "Снеговик",
                 "description": "Desc",
                 "trailer": "link",
                 "year": 2017,
                 "rating": 5.0,
                 "genre_id": 1,
                 "director_id": 2
                 }
        new_movie = movies_dao.create(movie)
        assert new_movie.title == movie.get("title")
