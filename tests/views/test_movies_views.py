import pytest

from project.models import Movie


class TestMoviesView:
    @pytest.fixture
    def movie_1(self, db):
        movie = Movie(
            id=1,
            title="Ночные звери",
            description="Desc",
            trailer="link",
            year=2016,
            rating=5.0,
            genre_id=1,
            director_id=2
        )
        db.session.add(movie)
        db.session.commit()
        return movie

    @pytest.fixture
    def movie_2(self, db):
        movie = Movie(
            id=2,
            title="Исчезнувшая",
            description="Desc",
            trailer="link",
            year=2017,
            rating=5.0,
            genre_id=1,
            director_id=2
        )
        db.session.add(movie)
        db.session.commit()
        return movie

    @pytest.fixture
    def movie_3(self, db):
        movie = Movie(
            id=3,
            title="Элизабеттаун",
            description="Desc",
            trailer="link",
            year=2005,
            rating=5.0,
            genre_id=1,
            director_id=2
        )
        db.session.add(movie)
        db.session.commit()
        return movie

    @pytest.fixture
    def movie_4(self, db):
        movie = Movie(
            id=4,
            title="Снеговик",
            description="Desc",
            trailer="link",
            year=2017,
            rating=5.0,
            genre_id=1,
            director_id=2
        )
        db.session.add(movie)
        db.session.commit()
        return movie

    def test_many(self, client, movie_1, movie_2, movie_3):
        response = client.get('/movies/')
        assert response.status_code == 200
        assert response.json == [
            {
                "id": movie_1.id,
                "title": movie_1.title,
                'description': 'Desc',
                'director': {'id': None, 'name': None},
                'genre': {'id': None, 'name': None},
                "trailer": movie_1.trailer,
                "year": movie_1.year,
                "rating": movie_1.rating,
                "genre_id": movie_1.genre_id,
                "director_id": movie_1.director_id
            },
            {
                "id": movie_2.id,
                "title": movie_2.title,
                'description': 'Desc',
                'director': {'id': None, 'name': None},
                'genre': {'id': None, 'name': None},
                "trailer": movie_2.trailer,
                "year": movie_2.year,
                "rating": movie_2.rating,
                "genre_id": movie_2.genre_id,
                "director_id": movie_2.director_id
            },
            {
                "id": movie_3.id,
                "title": movie_3.title,
                'description': 'Desc',
                'director': {'id': None, 'name': None},
                'genre': {'id': None, 'name': None},
                "trailer": movie_3.trailer,
                "year": movie_3.year,
                "rating": movie_3.rating,
                "genre_id": movie_3.genre_id,
                "director_id": movie_3.director_id
            }
        ]

    def test_movie_pages(self, client, movie_1, movie_2, movie_3):
        response = client.get('/movies/?page=1')
        assert response.status_code == 200
        assert len(response.json) == 3

        response = client.get('/movies/?page=2')
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_movie(self, client, movie_1):
        response = client.get('/movies/1/')
        assert response.status_code == 200
        assert response.json == {
            "id": movie_1.id,
            "title": movie_1.title,
            'description': 'Desc',
            'director': {'id': None, 'name': None},
            'genre': {'id': None, 'name': None},
            "trailer": movie_1.trailer,
            "year": movie_1.year,
            "rating": movie_1.rating,
            "genre_id": movie_1.genre_id,
            "director_id": movie_1.director_id}

    def test_movie_not_found(self, db, client):
        response = client.get('/movies/342/')
        assert response.status_code == 404
