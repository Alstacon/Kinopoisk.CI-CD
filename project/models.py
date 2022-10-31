from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from project.setup.db import models, db


class Genre(models.Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)

    movies = db.relationship("Movie", back_populates='genre')


class Director(models.Base):
    __tablename__ = 'director'

    name = Column(String(100), unique=True, nullable=False)

    movies = db.relationship("Movie", back_populates='director')


class Movie(models.Base):
    __tablename__ = 'movie'

    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    trailer = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    genre_id = Column(Integer, ForeignKey(f'{Genre.__tablename__}.id'), nullable=False)
    director_id = Column(Integer, ForeignKey(f'{Director.__tablename__}.id'), nullable=False)

    genre = db.relationship("Genre", back_populates='movies')
    director = db.relationship("Director", back_populates='movies')


# class Favorites(db.Model):
#     __tablename__ = 'favorites'
#
#     user_id = Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
#     movie_id = Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True, nullable=False)

favorites = db.Table(
    'favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True, nullable=False)
)


class User(models.Base):
    __tablename__ = 'user'

    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, unique=True)
    surname = Column(String)
    favorite_film = Column(Integer, ForeignKey(f'{Movie.__tablename__}.id'))

    favorites = db.relationship(
        Movie,
        secondary=favorites,
        lazy='subquery',
        backref=db.backref('movie', lazy=True)
    )
