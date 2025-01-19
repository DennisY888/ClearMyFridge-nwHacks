from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    preferred_name = db.Column(db.String(100))
    preferences = db.relationship('UserPreference', backref='user', lazy=True)
    fridge_items = db.relationship('UserFridge', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Preference(db.Model):
    __tablename__ = 'preferences'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    preference = db.Column(db.String(50), nullable=False, unique=True)
    users = db.relationship('UserPreference', backref='preference', lazy=True)


class UserPreference(db.Model):
    __tablename__ = 'user_preferences'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('auth.id'), nullable=False)
    preference_id = db.Column(db.Integer, db.ForeignKey('preferences.id'), nullable=False)

class UserFridge(db.Model):
    __tablename__ = 'user_fridge'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('auth.id'), nullable=False)
    ingredient_name = db.Column(db.String(100), nullable=False)
    purchase_date = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    expiry_date = db.Column(db.String(10), nullable=False)