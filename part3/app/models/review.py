from app import db
from .base_model import BaseModel
import uuid

class Review(BaseModel, db.Model):
    __tablename__ = 'reviews'
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # Relationship with Place and User handled by backref
    # place_id y user_id se agregan en Task 8
