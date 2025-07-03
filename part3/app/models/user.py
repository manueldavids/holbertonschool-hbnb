"""
User model for the HBnB application.
Handles user data and password hashing with bcrypt.
"""

import uuid
from datetime import datetime
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

# Import db from app.__init__
from app import db

# Initialize bcrypt for password hashing
bcrypt = Bcrypt()

# Import BaseModel
from .base_model import BaseModel


class User(BaseModel):
    """
    User model with password hashing capabilities.

    Attributes:
        id (str): Unique user identifier (UUID)
        email (str): User email address (unique)
        password_hash (str): Hashed password using bcrypt
        first_name (str): User's first name
        last_name (str): User's last name
        is_admin (bool): Admin privileges flag
        created_at (datetime): User creation timestamp
        updated_at (datetime): Last update timestamp
    """

    __tablename__ = 'users'

    # User information
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, email, password, first_name=None, last_name=None,
                 is_admin=False):
        """
        Initialize a new user with password hashing.

        Args:
            email (str): User email address
            password (str): Plain text password (will be hashed)
            first_name (str, optional): User's first name
            last_name (str, optional): User's last name
            is_admin (bool, optional): Admin privileges flag
        """
        super().__init__()  # Initialize BaseModel
        self.email = email.lower().strip() if email else None
        self.password_hash = self._hash_password(password)
        self.first_name = first_name.strip() if first_name else None
        self.last_name = last_name.strip() if last_name else None
        self.is_admin = bool(is_admin)

    def _hash_password(self, password):
        """
        Hash a password using bcrypt.

        Args:
            password (str): Plain text password

        Returns:
            str: Hashed password

        Raises:
            ValueError: If password is empty or None
        """
        if not password:
            raise ValueError("Password cannot be empty")
        
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Verify a password against the stored hash.

        Args:
            password (str): Plain text password to verify

        Returns:
            bool: True if password matches, False otherwise
        """
        if not password or not self.password_hash:
            return False
        
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        Convert user object to dictionary for JSON serialization.

        Note: Password hash is intentionally excluded for security.

        Returns:
            dict: User data without password information
        """
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def update_password(self, new_password):
        """
        Update user password with new hash.

        Args:
            new_password (str): New plain text password

        Raises:
            ValueError: If new password is empty or None
        """
        if not new_password:
            raise ValueError("New password cannot be empty")
        
        self.password_hash = self._hash_password(new_password)
        self.updated_at = datetime.utcnow()

    def update_profile(self, **kwargs):
        """
        Update user profile information.

        Args:
            **kwargs: Fields to update (email, first_name, last_name, is_admin)
        """
        allowed_fields = {'email', 'first_name', 'last_name', 'is_admin'}
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                if field == 'email' and value:
                    value = value.lower().strip()
                elif field in {'first_name', 'last_name'} and value:
                    value = value.strip()
                elif field == 'is_admin':
                    value = bool(value)
                
                setattr(self, field, value)
        
        self.updated_at = datetime.utcnow()

    @classmethod
    def create_user(cls, email, password, first_name=None, last_name=None,
                    is_admin=False):
        """
        Create a new user with password hashing.

        Args:
            email (str): User email address
            password (str): Plain text password
            first_name (str, optional): User's first name
            last_name (str, optional): User's last name
            is_admin (bool, optional): Admin privileges flag

        Returns:
            User: Newly created user instance

        Raises:
            ValueError: If email or password are invalid
        """
        if not email or not password:
            raise ValueError("Email and password are required")
        
        user = cls(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin
        )
        return user

    @classmethod
    def get_by_email(cls, email):
        """
        Get user by email address.

        Args:
            email (str): User email address

        Returns:
            User: User instance if found, None otherwise
        """
        if not email:
            return None
        
        return cls.query.filter_by(email=email.lower().strip()).first()

    @classmethod
    def get_by_id(cls, user_id):
        """
        Get user by ID.

        Args:
            user_id (str): User ID

        Returns:
            User: User instance if found, None otherwise
        """
        if not user_id:
            return None
        
        return cls.query.get(user_id)

    @classmethod
    def get_all_users(cls, limit=None, offset=0):
        """
        Get all users with optional pagination.

        Args:
            limit (int, optional): Maximum number of users to return
            offset (int, optional): Number of users to skip

        Returns:
            list: List of User instances
        """
        query = cls.query
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        
        return query.all()

    def __repr__(self):
        """String representation of the user."""
        return f'<User {self.email}>'

    def __str__(self):
        """String representation for display."""
        return f"User(id={self.id}, email={self.email})"
