"""
Repository pattern implementation for data persistence.
Provides abstraction layer for database operations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
from app import db


class Repository(ABC):
    """
    Abstract base class for repository pattern.
    Defines the interface for data access operations.
    """

    @abstractmethod
    def add(self, obj: Any) -> None:
        """
        Add a new object to the repository.

        Args:
            obj: Object to add
        """
        pass

    @abstractmethod
    def get(self, obj_id: str) -> Optional[Any]:
        """
        Get an object by its ID.

        Args:
            obj_id (str): Object ID to retrieve

        Returns:
            Object instance or None if not found
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Any]:
        """
        Get all objects from the repository.

        Returns:
            List of all objects
        """
        pass

    @abstractmethod
    def update(self, obj_id: str, data: Dict[str, Any]) -> Optional[Any]:
        """
        Update an object with new data.

        Args:
            obj_id (str): Object ID to update
            data (dict): Data to update

        Returns:
            Updated object or None if not found
        """
        pass

    @abstractmethod
    def delete(self, obj_id: str) -> bool:
        """
        Delete an object by its ID.

        Args:
            obj_id (str): Object ID to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        pass

    @abstractmethod
    def get_by_attribute(
            self,
            attr_name: str,
            attr_value: Any) -> Optional[Any]:
        """
        Get an object by a specific attribute value.

        Args:
            attr_name (str): Attribute name to search by
            attr_value: Attribute value to search for

        Returns:
            Object instance or None if not found
        """
        pass


class SQLAlchemyRepository(Repository):
    """
    SQLAlchemy implementation of the Repository interface.
    Handles database CRUD operations using SQLAlchemy ORM.
    """

    def __init__(self, model):
        """
        Initialize repository with a specific model.

        Args:
            model: SQLAlchemy model class
        """
        self.model = model

    def add(self, obj: Any) -> None:
        """
        Add a new object to the database.

        Args:
            obj: Object to add to the database
        """
        try:
            db.session.add(obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def get(self, obj_id: str) -> Optional[Any]:
        """
        Get an object by its ID from the database.

        Args:
            obj_id (str): Object ID to retrieve

        Returns:
            Object instance or None if not found
        """
        try:
            return self.model.query.get(obj_id)
        except Exception as e:
            print(f"Error getting object by ID: {str(e)}")
            return None

    def get_all(self) -> List[Any]:
        """
        Get all objects from the database.

        Returns:
            List of all objects
        """
        try:
            return self.model.query.all()
        except Exception as e:
            print(f"Error getting all objects: {str(e)}")
            return []

    def update(self, obj_id: str, data: Dict[str, Any]) -> Optional[Any]:
        """
        Update an object with new data.

        Args:
            obj_id (str): Object ID to update
            data (dict): Data to update

        Returns:
            Updated object or None if not found
        """
        try:
            obj = self.get(obj_id)
            if obj:
                for key, value in data.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                db.session.commit()
                return obj
            return None
        except Exception as e:
            db.session.rollback()
            print(f"Error updating object: {str(e)}")
            return None

    def delete(self, obj_id: str) -> bool:
        """
        Delete an object by its ID.

        Args:
            obj_id (str): Object ID to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            obj = self.get(obj_id)
            if obj:
                db.session.delete(obj)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting object: {str(e)}")
            return False

    def get_by_attribute(
            self,
            attr_name: str,
            attr_value: Any) -> Optional[Any]:
        """
        Get an object by a specific attribute value.

        Args:
            attr_name (str): Attribute name to search by
            attr_value: Attribute value to search for

        Returns:
            Object instance or None if not found
        """
        try:
            return self.model.query.filter_by(
                **{attr_name: attr_value}).first()
        except Exception as e:
            print(f"Error getting object by attribute: {str(e)}")
            return None

    def get_by_attributes(self, filters: Dict[str, Any]) -> List[Any]:
        """
        Get objects by multiple attribute filters.

        Args:
            filters (dict): Dictionary of attribute filters

        Returns:
            List of matching objects
        """
        try:
            return self.model.query.filter_by(**filters).all()
        except Exception as e:
            print(f"Error getting objects by attributes: {str(e)}")
            return []

    def count(self) -> int:
        """
        Get the total count of objects.

        Returns:
            Total number of objects
        """
        try:
            return self.model.query.count()
        except Exception as e:
            print(f"Error counting objects: {str(e)}")
            return 0
