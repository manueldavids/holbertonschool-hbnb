"""
Facade service for HBnB application.
Provides a unified interface for business operations.
"""

from typing import Optional, List, Dict, Any, Union
from flask import current_app
from app.models.user import User
from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app.persistence.repository import Repository
import uuid


class Facade:
    """
    Facade service providing unified business operations.
    Acts as a single point of entry for all business logic.
    """

    def __init__(self):
        """Initialize the facade with repositories."""
        self._user_repository = SQLAlchemyRepository(User)
        self._repositories: Dict[str, Repository] = {
            'user': self._user_repository,
            'place': SQLAlchemyRepository(Place)
        }

    # User Operations
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user.

        Args:
            user_data (dict): User data containing email, password, etc.

        Returns:
            dict: Created user data

        Raises:
            ValueError: If user data is invalid
            Exception: If user creation fails
        """
        try:
            user = self._user_repository.create_user(user_data)
            return user.to_dict()
        except ValueError as e:
            self._log_error(f"Validation error creating user: {e}")
            raise
        except Exception as e:
            self._log_error(f"Error creating user: {e}")
            raise

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user by ID.

        Args:
            user_id (str): User ID

        Returns:
            dict: User data if found, None otherwise

        Raises:
            Exception: If database operation fails
        """
        try:
            user = self._user_repository.get_user_by_id(user_id)
            return user.to_dict() if user else None
        except Exception as e:
            self._log_error(f"Error getting user {user_id}: {e}")
            raise

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email address.

        Args:
            email (str): User email address

        Returns:
            dict: User data if found, None otherwise

        Raises:
            Exception: If database operation fails
        """
        try:
            user = self._user_repository.get_user_by_email(email)
            return user.to_dict() if user else None
        except Exception as e:
            self._log_error(f"Error getting user by email {email}: {e}")
            raise

    def update_user(self, user_id: str,
                    update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update user information.

        Args:
            user_id (str): User ID to update
            update_data (dict): Data to update

        Returns:
            dict: Updated user data if found, None otherwise

        Raises:
            ValueError: If update data is invalid
            Exception: If database operation fails
        """
        try:
            user = self._user_repository.update_user(user_id, update_data)
            return user.to_dict() if user else None
        except ValueError as e:
            self._log_error(f"Validation error updating user {user_id}: {e}")
            raise
        except Exception as e:
            self._log_error(f"Error updating user {user_id}: {e}")
            raise

    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user.

        Args:
            user_id (str): User ID to delete

        Returns:
            bool: True if user was deleted, False if not found

        Raises:
            Exception: If database operation fails
        """
        try:
            return self._user_repository.delete_user(user_id)
        except Exception as e:
            self._log_error(f"Error deleting user {user_id}: {e}")
            raise

    def authenticate_user(
            self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with email and password.

        Args:
            email (str): User email address
            password (str): Plain text password

        Returns:
            dict: User data if authentication successful, None otherwise

        Raises:
            Exception: If database operation fails
        """
        try:
            user = self._user_repository.authenticate_user(email, password)
            return user.to_dict() if user else None
        except Exception as e:
            self._log_error(f"Error authenticating user {email}: {e}")
            raise

    def get_all_users(self, limit: Optional[int] = None,
                      offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get all users with optional pagination.

        Args:
            limit (int, optional): Maximum number of users to return
            offset (int, optional): Number of users to skip

        Returns:
            list: List of user data dictionaries

        Raises:
            Exception: If database operation fails
        """
        try:
            users = self._user_repository.get_all_users(
                limit=limit, offset=offset)
            return [user.to_dict() for user in users]
        except Exception as e:
            self._log_error(f"Error getting all users: {e}")
            raise

    def search_users(self, search_term: str,
                     limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search users by email, first name, or last name.

        Args:
            search_term (str): Search term
            limit (int, optional): Maximum number of results

        Returns:
            list: List of matching user data dictionaries

        Raises:
            Exception: If database operation fails
        """
        try:
            users = self._user_repository.search_users(
                search_term, limit=limit)
            return [user.to_dict() for user in users]
        except Exception as e:
            self._log_error(
                f"Error searching users with term '{search_term}': {e}")
            raise

    def get_users_by_admin_status(
            self, is_admin: bool) -> List[Dict[str, Any]]:
        """
        Get users by admin status.

        Args:
            is_admin (bool): Admin status to filter by

        Returns:
            list: List of user data dictionaries with specified admin status

        Raises:
            Exception: If database operation fails
        """
        try:
            users = self._user_repository.get_users_by_admin_status(is_admin)
            return [user.to_dict() for user in users]
        except Exception as e:
            self._log_error(
                f"Error getting users by admin status {is_admin}: {e}")
            raise

    # Generic Repository Operations
    def get_entity(self, entity_type: str,
                   entity_id: str) -> Optional[Dict[str, Any]]:
        """
        Get entity by type and ID.

        Args:
            entity_type (str): Type of entity (e.g., 'user')
            entity_id (str): Entity ID

        Returns:
            dict: Entity data if found, None otherwise

        Raises:
            ValueError: If entity type is not supported
            Exception: If database operation fails
        """
        try:
            repository = self._get_repository(entity_type)
            entity = repository.get(entity_id)
            return entity.to_dict() if entity else None
        except ValueError as e:
            self._log_error(f"Repository error: {e}")
            raise
        except Exception as e:
            self._log_error(f"Error getting {entity_type} {entity_id}: {e}")
            raise

    def get_all_entities(self, entity_type: str, limit: Optional[int] = None,
                         offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get all entities of a specific type.

        Args:
            entity_type (str): Type of entity (e.g., 'user')
            limit (int, optional): Maximum number of entities to return
            offset (int, optional): Number of entities to skip

        Returns:
            list: List of entity data dictionaries

        Raises:
            ValueError: If entity type is not supported
            Exception: If database operation fails
        """
        try:
            repository = self._get_repository(entity_type)
            entities = repository.get_all(limit=limit, offset=offset)
            return [entity.to_dict() for entity in entities]
        except ValueError as e:
            self._log_error(f"Repository error: {e}")
            raise
        except Exception as e:
            self._log_error(f"Error getting all {entity_type} entities: {e}")
            raise

    def create_entity(self, entity_type: str,
                      entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new entity of a specific type.

        Args:
            entity_type (str): Type of entity (e.g., 'user')
            entity_data (dict): Entity data

        Returns:
            dict: Created entity data

        Raises:
            ValueError: If entity type is not supported or data is invalid
            Exception: If entity creation fails
        """
        try:
            repository = self._get_repository(entity_type)

            # Use specific creation method for users
            if entity_type == 'user':
                entity = repository.create_user(entity_data)
            else:
                entity = repository.create(entity_data)

            return entity.to_dict()
        except ValueError as e:
            self._log_error(f"Validation error creating {entity_type}: {e}")
            raise
        except Exception as e:
            self._log_error(f"Error creating {entity_type}: {e}")
            raise

    def update_entity(self, entity_type: str, entity_id: str,
                      update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an entity of a specific type.

        Args:
            entity_type (str): Type of entity (e.g., 'user')
            entity_id (str): Entity ID to update
            update_data (dict): Data to update

        Returns:
            dict: Updated entity data if found, None otherwise

        Raises:
            ValueError: If entity type is not supported or data is invalid
            Exception: If database operation fails
        """
        try:
            repository = self._get_repository(entity_type)

            # Use specific update method for users
            if entity_type == 'user':
                entity = repository.update_user(entity_id, update_data)
            else:
                entity = repository.update(entity_id, update_data)

            return entity.to_dict() if entity else None
        except ValueError as e:
            self._log_error(f"Validation error updating {
                            entity_type} {entity_id}: {e}")
            raise
        except Exception as e:
            self._log_error(f"Error updating {entity_type} {entity_id}: {e}")
            raise

    def delete_entity(self, entity_type: str, entity_id: str) -> bool:
        """
        Delete an entity of a specific type.

        Args:
            entity_type (str): Type of entity (e.g., 'user')
            entity_id (str): Entity ID to delete

        Returns:
            bool: True if entity was deleted, False if not found

        Raises:
            ValueError: If entity type is not supported
            Exception: If database operation fails
        """
        try:
            repository = self._get_repository(entity_type)

            # Use specific delete method for users
            if entity_type == 'user':
                return repository.delete_user(entity_id)
            else:
                return repository.delete(entity_id)
        except ValueError as e:
            self._log_error(f"Repository error: {e}")
            raise
        except Exception as e:
            self._log_error(f"Error deleting {entity_type} {entity_id}: {e}")
            raise

    def _get_repository(self, entity_type: str) -> Repository:
        """
        Get repository for a specific entity type.

        Args:
            entity_type (str): Type of entity

        Returns:
            Repository: Repository instance

        Raises:
            ValueError: If entity type is not supported
        """
        repository = self._repositories.get(entity_type)
        if not repository:
            raise ValueError(f"Unsupported entity type: {entity_type}")
        return repository

    def _log_error(self, message: str) -> None:
        """
        Log error messages.

        Args:
            message (str): Error message to log
        """
        # In a production environment, this would use a proper logging system
        print(f"Facade Error: {message}")

    def __repr__(self) -> str:
        """String representation of the facade."""
        return f"<{self.__class__.__name__}>"

    # Place operations
    def create_place(self,
                     place_data: Dict[str,
                                      Any],
                     owner_id: str) -> Optional[Dict[str, Any]]:
        """
        Create a new place.

        Args:
            place_data (dict): Place data
            owner_id (str): ID of the place owner

        Returns:
            dict: Created place data or None if failed
        """
        try:
            # Generate UUID for place
            place_data['id'] = str(uuid.uuid4())
            place_data['owner_id'] = owner_id

            # Create place instance
            place = Place(**place_data)

            # Save to database using repository
            self._get_repository('place').add(place)

            return place.to_dict()

        except Exception as e:
            self._log_error(f"Error creating place: {str(e)}")
            return None

    def get_place(self, place_id: str) -> Optional[Dict[str, Any]]:
        """
        Get place by ID.

        Args:
            place_id (str): Place ID to retrieve

        Returns:
            dict: Place data if found, None otherwise
        """
        try:
            place = self._get_repository('place').get(place_id)
            return place.to_dict() if place else None
        except Exception as e:
            self._log_error(f"Error getting place {place_id}: {e}")
            raise

    def get_all_places(self) -> List[Dict[str, Any]]:
        """
        Get all places.

        Returns:
            list: List of place data dictionaries
        """
        try:
            places = self._get_repository('place').get_all()
            return [place.to_dict() for place in places]
        except Exception as e:
            self._log_error(f"Error getting all places: {e}")
            raise

    def get_places_by_owner(self, owner_id: str) -> List[Dict[str, Any]]:
        """
        Get all places owned by a specific user.

        Args:
            owner_id (str): Owner user ID

        Returns:
            list: List of place data dictionaries owned by the user
        """
        try:
            places = self._get_repository(
                'place').get_by_attribute('owner_id', owner_id)
            return [place.to_dict() for place in places]
        except Exception as e:
            self._log_error(f"Error getting places by owner {owner_id}: {e}")
            raise

    def update_place(self,
                     place_id: str,
                     place_data: Dict[str,
                                      Any]) -> Optional[Dict[str, Any]]:
        """
        Update place information.

        Args:
            place_id (str): Place ID to update
            place_data (dict): Data to update

        Returns:
            dict: Updated place data if found, None otherwise
        """
        try:
            place = self._get_repository('place').update(place_id, place_data)
            return place.to_dict() if place else None
        except Exception as e:
            self._log_error(f"Error updating place {place_id}: {e}")
            raise

    def delete_place(self, place_id: str) -> bool:
        """
        Delete place by ID.

        Args:
            place_id (str): Place ID to delete

        Returns:
            bool: True if deletion was successful
        """
        try:
            return self._get_repository('place').delete(place_id)
        except Exception as e:
            self._log_error(f"Error deleting place {place_id}: {e}")
            raise

    # Utility methods
    def validate_user_ownership(self, resource_id: str, user_id: str,
                                resource_type: str = 'place') -> bool:
        """
        Validate if a user owns a specific resource.

        Args:
            resource_id (str): Resource ID to check
            user_id (str): User ID to validate ownership
            resource_type (str): Type of resource ('place', 'user', etc.)

        Returns:
            bool: True if user owns the resource
        """
        if resource_type == 'place':
            place = self.get_place(resource_id)
            return place and str(place['owner_id']) == user_id
        elif resource_type == 'user':
            return resource_id == user_id

        return False

    def get_user_count(self) -> int:
        """
        Get total number of users.

        Returns:
            int: Total user count
        """
        return self._user_repository.count()

    def update_user_password(self, user_id: str, new_password: str) -> bool:
        """
        Update user password.

        Args:
            user_id (str): User ID to update
            new_password (str): New password

        Returns:
            bool: True if update was successful
        """
        return self._user_repository.update_user_password(
            user_id, new_password)

    def get_place_count(self) -> int:
        """
        Get total number of places.

        Returns:
            int: Total place count
        """
        return self._get_repository('place').count()
