"""
Base model class for SQLAlchemy models.
Provides common attributes and functionality for all models.
"""

import uuid
from datetime import datetime
from typing import Dict, Any
from app import db


class BaseModel(db.Model):
    """
    Abstract base model with common attributes.

    Attributes:
        id (str): Unique identifier (UUID)
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
    """

    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # Timestamps
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow,
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow,
        onupdate=datetime.utcnow, nullable=False
    )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model object to dictionary for JSON serialization.

        Returns:
            dict: Model data as dictionary
        """
        return {
            'id': self.id,
            'created_at': self._format_datetime(self.created_at),
            'updated_at': self._format_datetime(self.updated_at)
        }

    def update_timestamp(self) -> None:
        """
        Update the updated_at timestamp.
        """
        self.updated_at = datetime.utcnow()

    def _format_datetime(self, dt: datetime) -> str:
        """
        Format datetime for JSON serialization.

        Args:
            dt (datetime): Datetime to format

        Returns:
            str: ISO formatted datetime string or None
        """
        return dt.isoformat() if dt else None

    def __repr__(self) -> str:
        """
        String representation of the model.

        Returns:
            str: Model representation
        """
        return f"<{self.__class__.__name__}(id={self.id})>"

    def __str__(self) -> str:
        """
        String representation for display.

        Returns:
            str: Display string
        """
        return self.__repr__()
