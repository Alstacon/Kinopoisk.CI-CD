from project.config import BaseConfig
from project.models import Genre, Movie, Director, User
from project.server import create_app, db

config = BaseConfig()
app = create_app(config)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Director": Director,
        "Movie": Movie,
        "User": User,
    }
