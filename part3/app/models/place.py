"""
Place model for the HBnB application.
Defines the Place entity with SQLAlchemy ORM.
"""

from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base_model import BaseModel

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel, db.Model):
    """
    Place model representing properties available for booking.
    
    Attributes:
        id (UUID): Unique identifier for the place
        name (str): Name of the place
        description (str): Detailed description of the place
        address (str): Physical address of the place
        price_per_night (float): Price per night in currency units
        max_guests (int): Maximum number of guests allowed
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        owner_id (UUID): Foreign key to the owner user
        created_at (datetime): Timestamp when the place was created
        updated_at (datetime): Timestamp when the place was last updated
    """
    
    __tablename__ = 'places'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(256), nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                          onupdate=datetime.utcnow)
    
    # Relationship with User model
    owner = db.relationship('User', backref=db.backref('places', lazy='dynamic'))
    # Relationship with Review model
    reviews = db.relationship('Review', backref='place', lazy='dynamic')
    # Relationship with Amenity model
    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        backref=db.backref('places', lazy='dynamic'),
        lazy='dynamic'
    )
    
    def __init__(self, **kwargs):
        """Initialize a new Place instance."""
        super(Place, self).__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
    
    def to_dict(self):
        """
        Convert place object to dictionary.
        
        Returns:
            dict: Dictionary representation of the place
        """
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def update_from_dict(self, data):
        """
        Update place attributes from dictionary.
        
        Args:
            data (dict): Dictionary containing updated values
            
        Returns:
            bool: True if update was successful
        """
        try:
            for field, value in data.items():
                if hasattr(self, field) and value is not None:
                    setattr(self, field, value)
            self.updated_at = datetime.utcnow()
            return True
        except Exception:
            return False
    
    @classmethod
    def get_by_id(cls, place_id):
        """
        Get place by ID.
        
        Args:
            place_id (str): Place ID to search for
            
        Returns:
            Place: Place instance or None if not found
        """
        try:
            return cls.query.filter_by(id=place_id).first()
        except Exception:
            return None
    
    @classmethod
    def get_all(cls):
        """
        Get all places.
        
        Returns:
            list: List of all Place instances
        """
        try:
            return cls.query.all()
        except Exception:
            return []
    
    @classmethod
    def get_by_owner(cls, owner_id):
        """
        Get all places owned by a specific user.
        
        Args:
            owner_id (str): Owner user ID
            
        Returns:
            list: List of Place instances owned by the user
        """
        try:
            return cls.query.filter_by(owner_id=owner_id).all()
        except Exception:
            return []
    
    def __repr__(self):
        """String representation of the Place instance."""
        return f'<Place {self.name} (ID: {self.id})>' 
    
