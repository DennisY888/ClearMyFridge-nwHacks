import string
from flask import Blueprint, jsonify, request
from app.models import Auth, Preference, UserPreference, UserFridge
from app import db
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)


api = Blueprint('main', __name__)  # Fixed syntax


@api.route('/login', methods=['POST'])
def login():
    if not request.form.get('username') or not request.form.get('password'):
        return jsonify({'error': 'Missing credentials'}), 400
    
    user = Auth.query.filter_by(username=request.form['username']).first()
    if user and user.check_password(request.form['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'username': user.username
        }), 200
    return jsonify({'error': 'Invalid credentials'}), 401



@api.route('/register', methods=['POST'])
def register():
    if not request.form.get('username') or not request.form.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    if Auth.query.filter_by(username=request.form['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    user = Auth(
        username=request.form['username']
    )
    user.set_password(request.form['password'])

    preferences = request.form['preferences']
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Registration successful', 'username': user.username, "preferences": string(preferences)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500



@api.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = Auth.query.get(current_user_id)
    return jsonify({'message': f'Hello {user.username}!'}), 200