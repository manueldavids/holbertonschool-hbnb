"""
HBnB Facade service layer.
HBnB Facade service layer.
Provides a unified interface for business operations using
SQLAlchemy repository.
"""

from typing import List, Optional, Dict, Any
from app.models.user import User
from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository
import uuid


class HBnBFacade:
    """
    Facade class that provides a unified interface for HBnB operations.
    Uses SQLAlchemy repository for data persistence.
    """

    def __init__(self):
        """
        Initialize the facade with SQLAlchemy repositories.
        """
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)

    # User operations
    def create_user(self, user_data: Dict[str, Any]) -> Optional[User]:
        """
        Create a new user.

        Args:
            user_data (dict): User data containing email, password, etc.

        Returns:
            User: Created user instance or None if failed
        """
        try:
            # Generate UUID for user
            user_data['id'] = str(uuid.uuid4())

            # Create user instance
            user = User(**user_data)

            # Save to database using repository
            self.user_repo.add(user)

            return user

        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None

    def get_user(self, user_id: str) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id (str): User ID to retrieve

        Returns:
            User: User instance or None if not found
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.

        Args:
            email (str): Email address to search for

        Returns:
            User: User instance or None if not found
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self) -> List[User]:
        """
        Get all users.

        Returns:
            list: List of all User instances
        """
        return self.user_repo.get_all()

    def update_user(self,
                    user_id: str,
                    user_data: Dict[str,
                                    Any]) -> Optional[User]:
        """
        Update user information.

        Args:
            user_id (str): User ID to update
            user_data (dict): Data to update

        Returns:
            User: Updated user instance or None if failed
        """
        return self.user_repo.update(user_id, user_data)

    def delete_user(self, user_id: str) -> bool:
        """
        Delete user by ID.

        Args:
            user_id (str): User ID to delete

        Returns:
            bool: True if deletion was successful
        """
        return self.user_repo.delete(user_id)

    # Place operations
    def create_place(self,
                     place_data: Dict[str,
                                      Any],
                     owner_id: str) -> Optional[Place]:
        """
        Create a new place.

        Args:
            place_data (dict): Place data
            owner_id (str): ID of the place owner

        Returns:
            Place: Created place instance or None if failed
        """
        try:
            # Generate UUID for place
            place_data['id'] = str(uuid.uuid4())
            place_data['owner_id'] = owner_id

            # Create place instance
            place = Place(**place_data)

            # Save to database using repository
            self.place_repo.add(place)

            return place

        except Exception as e:
            print(f"Error creating place: {str(e)}")
            return None

    def get_place(self, place_id: str) -> Optional[Place]:
        """
        Get place by ID.

        Args:
            place_id (str): Place ID to retrieve

        Returns:
            Place: Place instance or None if not found
        """
        return self.place_repo.get(place_id)

    def get_all_places(self) -> List[Place]:
        """
        Get all places.

        Returns:
            list: List of all Place instances
        """
        return self.place_repo.get_all()

    def get_places_by_owner(self, owner_id: str) -> List[Place]:
        """
        Get all places owned by a specific user.

        Args:
            owner_id (str): Owner user ID

        Returns:
            list: List of Place instances owned by the user
        """
        return self.place_repo.get_by_attribute('owner_id', owner_id)

    def update_place(self,
                     place_id: str,
                     place_data: Dict[str,
                                      Any]) -> Optional[Place]:
        """
        Update place information.

        Args:
            place_id (str): Place ID to update
            place_data (dict): Data to update

        Returns:
            Place: Updated place instance or None if failed
        """
        return self.place_repo.update(place_id, place_data)

    def delete_place(self, place_id: str) -> bool:
        """
        Delete place by ID.

        Args:
            place_id (str): Place ID to delete

        Returns:
            bool: True if deletion was successful
        """
        return self.place_repo.delete(place_id)

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
            return place and str(place.owner_id) == user_id
        elif resource_type == 'user':
            return resource_id == user_id

        return False

    def get_user_count(self) -> int:
        """
        Get total number of users.

        Returns:
            int: Total user count
        """
        return self.user_repo.count()

    def get_place_count(self) -> int:
        """
        Get total number of places.

        Returns:
            int: Total place count
        """
        return self.place_repo.count()
