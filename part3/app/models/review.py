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

    def to_dict(self):
        """
        Convert review to dictionary for JSON serialization.
        """
        return {
            'id': self.id,
            'rating': self.rating,
            'comment': self.comment,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'created_at': self._format_datetime(self.created_at),
            'updated_at': self._format_datetime(self.updated_at)
        }
