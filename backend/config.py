from os import environ, path

basedir = path.abspath(path.dirname(__file__))

class Config:
    SECRET_KEY = environ.get('SECRET_KEY', 'dev-key')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{path.join(basedir, 'dev.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False