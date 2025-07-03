"""
Base model class for SQLAlchemy models.
Provides common attributes and functionality for all models.
"""

import uuid
from datetime import datetime
from app import db


class BaseModel(db.Model):
    """
    Abstract base model with common attributes.

    Attributes:
        id (str): Unique identifier (UUID)
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
    """

    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    # Primary key
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow,
                           nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        """
        Convert model object to dictionary for JSON serialization.

        Returns:
            dict: Model data as dictionary
        """
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None}

    def update_timestamp(self):
        """
        Update the updated_at timestamp.
        """
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        """
        String representation of the model.

        Returns:
            str: Model representation
        """
        return f"<{self.__class__.__name__}(id={self.id})>"
