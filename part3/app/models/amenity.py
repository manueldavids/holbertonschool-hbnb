"""
Amenity model for the HBnB application.
Defines the Amenity entity with SQLAlchemy ORM.
"""

from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Amenity(db.Model):
    """
    Amenity model representing available amenities for places.
    
    Attributes:
        id (UUID): Unique identifier for the amenity
        name (str): Name of the amenity
        description (str): Detailed description of the amenity
        created_at (datetime): Timestamp when the amenity was created
        updated_at (datetime): Timestamp when the amenity was last updated
    """
    
    __tablename__ = 'amenities'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                          onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        """Initialize a new Amenity instance."""
        super(Amenity, self).__init__(**kwargs)
        if not self.id:
            self.id = uuid.uuid4()
    
    def to_dict(self):
        """
        Convert amenity object to dictionary.
        
        Returns:
            dict: Dictionary representation of the amenity
        """
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def update_from_dict(self, data):
        """
        Update amenity attributes from dictionary.
        
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
    def get_by_id(cls, amenity_id):
        """
        Get amenity by ID.
        
        Args:
            amenity_id (str): Amenity ID to search for
            
        Returns:
            Amenity: Amenity instance or None if not found
        """
        try:
            return cls.query.filter_by(id=amenity_id).first()
        except Exception:
            return None
    
    @classmethod
    def get_by_name(cls, name):
        """
        Get amenity by name.
        
        Args:
            name (str): Amenity name to search for
            
        Returns:
            Amenity: Amenity instance or None if not found
        """
        try:
            return cls.query.filter_by(name=name).first()
        except Exception:
            return None
    
    @classmethod
    def get_all(cls):
        """
        Get all amenities.
        
        Returns:
            list: List of all Amenity instances
        """
        try:
            return cls.query.all()
        except Exception:
            return []
    
    @classmethod
    def create(cls, **kwargs):
        """
        Create a new amenity.
        
        Args:
            **kwargs: Amenity attributes (name, description)
            
        Returns:
            Amenity: New amenity instance or None if creation failed
        """
        try:
            amenity = cls(**kwargs)
            db.session.add(amenity)
            db.session.commit()
            return amenity
        except Exception as e:
            db.session.rollback()
            print(f"Error creating amenity: {e}")
            return None
    
    def delete(self):
        """
        Delete the amenity from database.
        
        Returns:
            bool: True if deletion was successful
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting amenity: {e}")
            return False
    
    def __repr__(self):
        """String representation of the Amenity instance."""
        return f'<Amenity {self.name} (ID: {self.id})>' 