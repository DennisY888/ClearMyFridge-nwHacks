from flask import Flask
from flask_cors import CORS
from config import Config
from app.extensions import db, jwt
from app.models import Preference

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    jwt.init_app(app)
    db.init_app(app)
    
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'app': app}
        
    from app.routes import api
    app.register_blueprint(api)
    
    with app.app_context():
        db.create_all()
        if not Preference.query.first():
            preferences = [
                'vegetarian', 'halal', 'kosher', 'gluten_free', 'lactose_free',
                'nut_free', 'soy_free', 'pescatarian', 'vegan', 'jain',
                'hindu_vegetarian', 'low_sugar', 'flexitarian', 'raw_vegan', 'low_sodium'
            ]
            for pref in preferences:
                db.session.add(Preference(preference=pref))
            db.session.commit()
            
    return app