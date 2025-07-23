"""
User model for the HBnB application.
Handles user data and password hashing with bcrypt.
"""

from typing import Optional, Dict, Any
from sqlalchemy.exc import IntegrityError
from app import db
from .base_model import BaseModel
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class User(BaseModel):
    """
    User model with password hashing capabilities.

    Attributes:
        email (str): User email address (unique)
        password_hash (str): Hashed password using bcrypt
        first_name (str): User's first name
        last_name (str): User's last name
        is_admin (bool): Admin privileges flag
    """

    __tablename__ = 'users'

    # User information
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Relationship: one user has many reviews
    reviews = db.relationship('Review', backref='user', lazy='dynamic')

    def __init__(
            self,
            email: str,
            password: str,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            is_admin: bool = False):
        """
        Initialize a new user with password hashing.

        Args:
            email (str): User email address
            password (str): Plain text password (will be hashed)
            first_name (str, optional): User's first name
            last_name (str, optional): User's last name
            is_admin (bool, optional): Admin privileges flag
        """
        super().__init__()
        self._validate_email(email)
        self._validate_password(password)

        self.email = self._normalize_email(email)
        self.password_hash = self._hash_password(password)
        self.first_name = self._normalize_name(first_name)
        self.last_name = self._normalize_name(last_name)
        self.is_admin = bool(is_admin)

    def _validate_email(self, email: str) -> None:
        """
        Validate email format and presence.

        Args:
            email (str): Email to validate

        Raises:
            ValueError: If email is invalid
        """
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")

        if '@' not in email or '.' not in email:
            raise ValueError("Invalid email format")

    def _validate_password(self, password: str) -> None:
        """
        Validate password strength and presence.

        Args:
            password (str): Password to validate

        Raises:
            ValueError: If password is invalid
        """
        if not password or not isinstance(password, str):
            raise ValueError("Password is required and must be a string")

        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")

    def _normalize_email(self, email: str) -> str:
        """
        Normalize email address.

        Args:
            email (str): Email to normalize

        Returns:
            str: Normalized email
        """
        return email.lower().strip() if email else None

    def _normalize_name(self, name: Optional[str]) -> Optional[str]:
        """
        Normalize name field.

        Args:
            name (str, optional): Name to normalize

        Returns:
            str: Normalized name or None
        """
        return name.strip() if name else None

    def _hash_password(self, password: str) -> str:
        """
        Hash a password using Flask-Bcrypt.

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

    def verify_password(self, password: str) -> bool:
        """
        Verify a password against the stored hash using Flask-Bcrypt.

        Args:
            password (str): Plain text password to verify

        Returns:
            bool: True if password matches, False otherwise
        """
        if not password or not self.password_hash:
            return False

        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert user object to dictionary for JSON serialization.

        Note: Password hash is intentionally excluded for security.

        Returns:
            dict: User data without password information
        """
        base_dict = super().to_dict()
        user_dict = {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin
        }
        base_dict.update(user_dict)
        return base_dict

    def update_password(self, new_password: str) -> None:
        """
        Update user password with new hash.

        Args:
            new_password (str): New plain text password

        Raises:
            ValueError: If new password is empty or None
        """
        self._validate_password(new_password)
        self.password_hash = self._hash_password(new_password)
        self.update_timestamp()

    def update_profile(self, **kwargs: Any) -> None:
        """
        Update user profile information.

        Args:
            **kwargs: Fields to update (email, first_name, last_name, is_admin)
        """
        allowed_fields = {'email', 'first_name', 'last_name', 'is_admin'}

        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                if field == 'email':
                    self._validate_email(value)
                    value = self._normalize_email(value)
                elif field in {'first_name', 'last_name'}:
                    value = self._normalize_name(value)
                elif field == 'is_admin':
                    value = bool(value)

                setattr(self, field, value)

        self.update_timestamp()

    @classmethod
    def create_user(
            cls,
            email: str,
            password: str,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            is_admin: bool = False) -> 'User':
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
        return cls(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin
        )

    @classmethod
    def get_by_email(cls, email: str) -> Optional['User']:
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
    def get_by_id(cls, user_id: str) -> Optional['User']:
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
    def get_all_users(
            cls,
            limit: Optional[int] = None,
            offset: int = 0) -> list['User']:
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

    def __repr__(self) -> str:
        """String representation of the user."""
        return f'<User {self.email}>'

    def __str__(self) -> str:
        """String representation for display."""
        return f"User(id={self.id}, email={self.email})"
