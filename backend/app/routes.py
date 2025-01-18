from flask import Blueprint, jsonify, request
from app.models import Recipe
from app import db


api = Blueprint('main', __name__)

@api.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'ingredients': r.ingredients,
        'instructions': r.instructions
    } for r in recipes])


@api.route('/api/recipes', methods=['POST'])
def create_recipe():
    data = request.json
    recipe = Recipe(
        name=data['name'],
        ingredients=data['ingredients'],
        instructions=data['instructions']
    )
    db.session.add(recipe)
    db.session.commit()
    return jsonify({'id': recipe.id}), 201


@api.route('/login', methods=['POST'])
def login():
    return jsonify({'id': "nigga"}), 201