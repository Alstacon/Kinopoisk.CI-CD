from unittest.mock import patch

import pytest

from project.exceptions import ItemNotFound
from project.models import Movie
from project.services import MoviesService


class TestMoviesService:

    @pytest.fixture()
    @patch('project.dao.MoviesDAO')
    def movies_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_by_id.return_value = Movie(title="Test_movie_1",
                                           description="Desc",
                                           trailer="link",
                                           year=2017,
                                           rating=5.0,
                                           genre_id=1,
                                           director_id=2
                                           )
        dao.get_all.return_value = [
            Movie(title="Test_movie_1",
                  description="Desc",
                  trailer="link",
                  year=2017,
                  rating=5.0,
                  genre_id=1,
                  director_id=2
                  ),
            Movie(title="Test_movie_2",
                  description="Desc",
                  trailer="link",
                  year=2000,
                  rating=25.0,
                  genre_id=14,
                  director_id=6
                  )
        ]

        return dao

    @pytest.fixture()
    def movies_service(self, movies_dao_mock):
        return MoviesService(dao=movies_dao_mock)

    @pytest.fixture
    def movie(self, db):
        m = Movie(title="Test_movie_3",
                  description="Desc",
                  trailer="link",
                  year=1998,
                  rating=3.0,
                  genre_id=12,
                  director_id=12
                  )
        db.session.add(m)
        db.session.commit()
        return m

    def test_get_movie(self, movies_service):
        movie = movies_service.get_item(1)
        assert movie.title == 'Test_movie_1'

    def test_movie_not_found(self, movies_dao_mock, movies_service):
        movies_dao_mock.get_by_id.return_value = None
        with pytest.raises(ItemNotFound):
            movies_service.get_item(987)

    @pytest.mark.parametrize('page', [1, None])
    def test_get_all_movies(self, movies_service, movies_dao_mock, page):
        movies = movies_service.get_all(page=page)
        assert len(movies) == 2
        assert movies == movies_dao_mock.get_all.return_value
        movies_dao_mock.get_all.assert_called_with(page=page)

