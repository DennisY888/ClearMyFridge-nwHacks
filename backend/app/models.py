from app import db
from datetime import datetime

class Recipe(db.Model):
   __tablename__ = 'recipes'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   ingredients = db.Column(db.String(500), nullable=False)
   instructions = db.Column(db.Text, nullable=False)
   created_at = db.Column(db.DateTime, default=datetime.utcnow)
