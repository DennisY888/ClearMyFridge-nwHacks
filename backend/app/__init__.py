from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    jwt.init_app(app)
    db.init_app(app)
    
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'app': app}
    
    from app import models
    from app.routes import api
    app.register_blueprint(api)
    return app