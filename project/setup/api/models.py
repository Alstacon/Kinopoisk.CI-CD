from flask_restx import fields, Model

from project.setup.api import api

genre_model: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director_model: Model = api.model('Директор', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Тим Бертон'),
})

movie_model: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_lenght=100, example='Йеллоустоун'),
    'description': fields.String(required=True, max_lenght=100, example='Описание'),
    'trailer': fields.String(required=True, max_lenght=100, example='https://www.youtube.com/watch?v=nDzZvwtBSJk'),
    'year': fields.Integer(required=True, example=2000),
    'rating': fields.Float(required=True, example=6.7),
    'genre_id': fields.Integer(required=True, example=1),
    'director_id': fields.Integer(required=True, example=1),
    'genre': fields.Nested(genre_model),
    'director': fields.Nested(director_model)
})

favorites_model = api.model('Избранное', {
        'user_id': fields.Integer(required=True, example=1),
        'movie_id': fields.Integer(required=True, example=1),
    }
)

user_model: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, example="email"),
    'password': fields.String(required=True, example="password"),
    'name': fields.String(required=True, example='name'),
    'surname': fields.String(required=True, example='surname'),
    'favorites': fields.Nested(movie_model)
})


tokens_model: Model = api.model( 'Токены', {
    'access_token': fields.String(required=True, example='eyJ0UzI1NiJ9.eyJpwijYyNzIwNzM3fQ.r-FJx1OFp1pDSmwc4lRM'),
    'refresh_token': fields.String(required=True, example='eyJ0UzI1NiJ9.eyJpwijYyNzIwNzM3fQ.r-FJx1OFp1pDSmwcikhM')
})
