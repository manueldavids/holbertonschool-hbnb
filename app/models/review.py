from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    # ... other fields ...

    def __repr__(self):
        return f'<Review {self.id}>' 