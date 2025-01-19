from os import environ, path
basedir = path.abspath(path.dirname(__file__))
from os import environ, path
from datetime import timedelta  

basedir = path.abspath(path.dirname(__file__))

class Config:
    SECRET_KEY = environ.get('SECRET_KEY', 'dev-key')
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', f"sqlite:///{path.join(basedir, 'dev.db')}")
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY', 'dev-jwt-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

