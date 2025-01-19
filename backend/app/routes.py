import string
from flask import Blueprint, jsonify, request
from datetime import datetime
from app.models import Auth, Preference, UserPreference, UserFridge
from app.extensions import db, jwt, token_blocklist
from flask_jwt_extended import (
   create_access_token,
   create_refresh_token, 
   get_jwt,
   jwt_required,
   get_jwt_identity
)



api = Blueprint('main', __name__)



@api.route('/refresh', methods=['GET'])
# @jwt_required(refresh=True)
def refresh():
   current_user_id = get_jwt_identity()
   access_token = create_access_token(identity=current_user_id)
   return jsonify({'access_token': access_token}), 200



@api.route('/logout', methods=['POST'])
# @jwt_required()
def logout():
   jti = get_jwt()["jti"]
   token_blocklist.add(jti)
   return jsonify({'message': 'Successfully logged out'}), 200



@api.route('/login', methods=['POST'])
def login():
   if not request.form.get('username') or not request.form.get('password'):
       return jsonify({'error': 'Missing credentials'}), 400

   user = Auth.query.filter_by(username=request.form['username']).first()

   if user and user.check_password(request.form['password']):
       access_token = create_access_token(identity=user.id)
       refresh_token = create_refresh_token(identity=user.id)

       # NEW CODE START
       # Fetch user preferences using the relationship defined in your models
       user_preferences = user.preferences

       # Create a list to store the preference names as strings
       preference_list = [pref.preference.preference for pref in user_preferences]

       # Fetch user ingredients using the relationship defined in your models
       user_ingredients = [
           {
               "ingredient_name": ingredient.ingredient_name,
               "purchase_date": ingredient.purchase_date.strftime("%Y-%m-%d %H:%M:%S"),  # Format datetime for JSON
               "quantity": ingredient.quantity,
               "expiry_date": ingredient.expiry_date.strftime("%Y-%m-%d %H:%M:%S"),
           }
           for ingredient in user.fridge_items
       ]
       # NEW CODE END

       return jsonify({
           'access_token': access_token,  # Include access token
           'refresh_token': refresh_token,  # Include refresh token
           'preferences': preference_list,
           'ingredients': user_ingredients  # NEW CODE: Added ingredients to the response
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

    preferences_string = request.form['preferences']
    # Lowercase and replace spaces and hyphens with underscores for each preference
    preferences_list = [preference.lower().replace(' ', '_').replace('-', '_') for preference in preferences_string.strip(',').split(',')]

    try:
        db.session.add(user)
        db.session.flush()

        # NEW CODE START
        for preference_name in preferences_list:
            preference_object = Preference.query.filter_by(preference=preference_name).first()
            if preference_object is None:
                db.session.rollback()
                return jsonify({'error': f'Preference "{preference_name}" does not exist.'}), 400
            user_preference = UserPreference(user_id=user.id, preference_id=preference_object.id)
            db.session.add(user_preference)
        # NEW CODE END

        db.session.commit()

        # Generate access and refresh tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            "message": "Registration successful",
            "user_id": user.id,
            "username": user.username,
            "preferences": str(preferences_list)[1:-1],  # Remove brackets from preference list
            "access_token": access_token,
            "refresh_token": refresh_token,
            'access_token': access_token
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500




@api.route('/add_ingredient', methods=['POST'])
# @jwt_required()
def add_ingredient():
    # current_user_id = get_jwt_identity()
    current_user_id = request.form["user_id"]

    if not all(k in request.form for k in ['ingredient_name', 'purchase_date', 'quantity']):
        return jsonify({'error': 'Missing required fields'}), 400

    if request.form['quantity'] not in ['alittle', 'some', 'alot']:
        return jsonify({'error': 'Invalid quantity value'}), 400

    expiry_date = datetime(2025, 12, 31, 23, 59, 59)

    try:
        purchase_date = datetime.strptime(request.form['purchase_date'], '%Y-%m-%d')
        purchase_date = purchase_date.replace(hour=0, minute=0, second=0)
    except ValueError:
        return jsonify({'error': 'Invalid date format for purchase_date. Use YYYY-MM-DD HH:MM:SS'}), 400

    try:
        ingredient = UserFridge(
            user_id=current_user_id,
            ingredient_name=request.form['ingredient_name'],
            purchase_date=purchase_date,
            quantity=request.form['quantity'],
            expiry_date=expiry_date
        )
        db.session.add(ingredient)
        db.session.commit()
        return jsonify({
            'message': 'Ingredient added successfully',
            'ingredient': {
                'name': ingredient.ingredient_name,
                'purchase_date': ingredient.purchase_date,
                'quantity': ingredient.quantity
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add ingredient', 'details': str(e)}), 500





@api.route('/protected', methods=['GET'])
# @jwt_required()
def protected():
   current_user_id = get_jwt_identity()
   user = Auth.query.get(current_user_id)
   return jsonify({'message': f'Hello {user.username}!'}), 200


