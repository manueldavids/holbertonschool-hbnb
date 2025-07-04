"""
User repository for database operations.
Handles user-specific database queries and operations.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app import db
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """
    Repository for User model operations.
    Provides user-specific database queries and operations.
    """

    def __init__(self):
        """Initialize the user repository."""
        super().__init__(User)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.

        Args:
            email (str): User email address

        Returns:
            User: User instance if found, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            if not email:
                return None

            normalized_email = email.lower().strip()
            return User.query.filter_by(email=normalized_email).first()
        except SQLAlchemyError as e:
            self._log_error(f"Error getting user by email {email}: {e}")
            raise

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id (str): User ID

        Returns:
            User: User instance if found, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            if not user_id:
                return None

            return User.query.get(user_id)
        except SQLAlchemyError as e:
            self._log_error(f"Error getting user by ID {user_id}: {e}")
            raise

    def create_user(self, user_data: Dict[str, Any]) -> User:
        """
        Create a new user.

        Args:
            user_data (dict): User data containing email, password, etc.

        Returns:
            User: Newly created user instance

        Raises:
            ValueError: If required data is missing or invalid
            IntegrityError: If user with same email already exists
            SQLAlchemyError: If database operation fails
        """
        try:
            # Validate required fields
            self._validate_user_data(user_data)

            # Create user instance
            user = User.create_user(
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
                is_admin=user_data.get('is_admin', False)
            )

            # Save to database
            db.session.add(user)
            db.session.commit()

            return user

        except IntegrityError as e:
            db.session.rollback()
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(
                    f"User with email {
                        user_data.get('email')} already exists")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            self._log_error(f"Error creating user: {e}")
            raise
        except Exception as e:
            db.session.rollback()
            self._log_error(f"Unexpected error creating user: {e}")
            raise

    def update_user(self,
                    user_id: str,
                    update_data: Dict[str,
                                      Any]) -> Optional[User]:
        """
        Update user information.

        Args:
            user_id (str): User ID to update
            update_data (dict): Data to update

        Returns:
            User: Updated user instance if found, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return None

            # Update user profile
            user.update_profile(**update_data)

            # Save changes
            db.session.commit()
            return user

        except IntegrityError as e:
            db.session.rollback()
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(
                    f"Email {
                        update_data.get('email')} already exists")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            self._log_error(f"Error updating user {user_id}: {e}")
            raise

    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user by ID.

        Args:
            user_id (str): User ID to delete

        Returns:
            bool: True if user was deleted, False if not found

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False

            db.session.delete(user)
            db.session.commit()
            return True

        except SQLAlchemyError as e:
            db.session.rollback()
            self._log_error(f"Error deleting user {user_id}: {e}")
            raise

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password.

        Args:
            email (str): User email address
            password (str): Plain text password

        Returns:
            User: User instance if authentication successful, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            user = self.get_user_by_email(email)
            if not user:
                return None

            if user.verify_password(password):
                return user

            return None

        except SQLAlchemyError as e:
            self._log_error(f"Error authenticating user {email}: {e}")
            raise

    def get_all_users(self, limit: Optional[int] = None,
                      offset: int = 0) -> List[User]:
        """
        Get all users with optional pagination.

        Args:
            limit (int, optional): Maximum number of users to return
            offset (int, optional): Number of users to skip

        Returns:
            list: List of User instances

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            return User.get_all_users(limit=limit, offset=offset)
        except SQLAlchemyError as e:
            self._log_error(f"Error getting all users: {e}")
            raise

    def search_users(
            self,
            search_term: str,
            limit: Optional[int] = None) -> List[User]:
        """
        Search users by email, first name, or last name.

        Args:
            search_term (str): Search term
            limit (int, optional): Maximum number of results

        Returns:
            list: List of matching User instances

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            if not search_term:
                return []

            query = User.query.filter(
                db.or_(
                    User.email.ilike(f'%{search_term}%'),
                    User.first_name.ilike(f'%{search_term}%'),
                    User.last_name.ilike(f'%{search_term}%')
                )
            )

            if limit:
                query = query.limit(limit)

            return query.all()

        except SQLAlchemyError as e:
            self._log_error(
                f"Error searching users with term '{search_term}': {e}")
            raise

    def get_users_by_admin_status(self, is_admin: bool) -> List[User]:
        """
        Get users by admin status.

        Args:
            is_admin (bool): Admin status to filter by

        Returns:
            list: List of User instances with specified admin status

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            return User.query.filter_by(is_admin=is_admin).all()
        except SQLAlchemyError as e:
            self._log_error(
                f"Error getting users by admin status {is_admin}: {e}")
            raise

    def update_user_password(self, user_id: str, new_password: str) -> bool:
        """
        Update user password.

        Args:
            user_id (str): User ID to update
            new_password (str): New password

        Returns:
            bool: True if update was successful, False otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False

            # Validate password strength
            if not new_password or len(new_password) < 6:
                raise ValueError("Password must be at least 6 characters long")

            # Update password
            user.update_password(new_password)

            # Save changes
            db.session.commit()
            return True

        except ValueError as e:
            db.session.rollback()
            self._log_error(f"Validation error updating password for user {user_id}: {e}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            self._log_error(f"Error updating password for user {user_id}: {e}")
            raise

    def _validate_user_data(self, user_data: Dict[str, Any]) -> None:
        """
        Validate user data before creation.

        Args:
            user_data (dict): User data to validate

        Raises:
            ValueError: If required data is missing or invalid
        """
        required_fields = ['email', 'password']

        for field in required_fields:
            if field not in user_data or not user_data[field]:
                raise ValueError(f"Field '{field}' is required")

        # Validate email format
        email = user_data['email']
        if not isinstance(email, str) or '@' not in email or '.' not in email:
            raise ValueError("Invalid email format")

        # Validate password strength
        password = user_data['password']
        if not isinstance(password, str) or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")

    def _log_error(self, message: str) -> None:
        """
        Log error messages.

        Args:
            message (str): Error message to log
        """
        # In a production environment, this would use a proper logging system
        print(f"UserRepository Error: {message}")
