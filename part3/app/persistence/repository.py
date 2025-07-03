"""
Repository pattern implementation for data persistence.
Provides abstraction layer for database operations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict, TypeVar, Generic, Type
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from app import db

# Generic type for models
T = TypeVar('T')


class Repository(Generic[T]):
    """
    Generic repository for database operations.
    Provides common CRUD operations for any SQLAlchemy model.

    Attributes:
        model (Type[T]): The SQLAlchemy model class
    """

    def __init__(self, model: Type[T]):
        """
        Initialize repository with a model class.

        Args:
            model (Type[T]): SQLAlchemy model class
        """
        self.model = model

    def get(self, entity_id: str) -> Optional[T]:
        """
        Get entity by ID.

        Args:
            entity_id (str): Entity ID

        Returns:
            T: Entity instance if found, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            if not entity_id:
                return None

            return self.model.query.get(entity_id)
        except SQLAlchemyError as e:
            self._log_error(
                f"Error getting {
                    self.model.__name__} with ID {entity_id}: {e}")
            raise

    def get_all(self, limit: Optional[int] = None,
                offset: int = 0) -> List[T]:
        """
        Get all entities with optional pagination.

        Args:
            limit (int, optional): Maximum number of entities to return
            offset (int, optional): Number of entities to skip

        Returns:
            list: List of entity instances

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            query = self.model.query

            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)

            return query.all()
        except SQLAlchemyError as e:
            self._log_error(
                f"Error getting all {
                    self.model.__name__} entities: {e}")
            raise

    def create(self, entity_data: Dict[str, Any]) -> T:
        """
        Create a new entity.

        Args:
            entity_data (dict): Entity data

        Returns:
            T: Newly created entity instance

        Raises:
            ValueError: If required data is missing
            IntegrityError: If unique constraint is violated
            SQLAlchemyError: If database operation fails
        """
        try:
            # Validate required data
            self._validate_entity_data(entity_data)

            # Create entity instance
            entity = self.model(**entity_data)

            # Save to database
            db.session.add(entity)
            db.session.commit()

            return entity

        except IntegrityError as e:
            db.session.rollback()
            self._handle_integrity_error(e)
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            self._log_error(f"Error creating {self.model.__name__}: {e}")
            raise
        except Exception as e:
            db.session.rollback()
            self._log_error(
                f"Unexpected error creating {
                    self.model.__name__}: {e}")
            raise

    def update(self,
               entity_id: str,
               update_data: Dict[str,
                                 Any]) -> Optional[T]:
        """
        Update an entity.

        Args:
            entity_id (str): Entity ID to update
            update_data (dict): Data to update

        Returns:
            T: Updated entity instance if found, None otherwise

        Raises:
            IntegrityError: If unique constraint is violated
            SQLAlchemyError: If database operation fails
        """
        try:
            entity = self.get(entity_id)
            if not entity:
                return None

            # Update entity attributes
            for key, value in update_data.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)

            # Update timestamp if available
            if hasattr(entity, 'update_timestamp'):
                entity.update_timestamp()

            # Save changes
            db.session.commit()
            return entity

        except IntegrityError as e:
            db.session.rollback()
            self._handle_integrity_error(e)
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            self._log_error(
                f"Error updating {
                    self.model.__name__} {entity_id}: {e}")
            raise

    def delete(self, entity_id: str) -> bool:
        """
        Delete an entity by ID.

        Args:
            entity_id (str): Entity ID to delete

        Returns:
            bool: True if entity was deleted, False if not found

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            entity = self.get(entity_id)
            if not entity:
                return False

            db.session.delete(entity)
            db.session.commit()
            return True

        except SQLAlchemyError as e:
            db.session.rollback()
            self._log_error(
                f"Error deleting {
                    self.model.__name__} {entity_id}: {e}")
            raise

    def count(self) -> int:
        """
        Get total count of entities.

        Returns:
            int: Total number of entities

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            return self.model.query.count()
        except SQLAlchemyError as e:
            self._log_error(
                f"Error counting {
                    self.model.__name__} entities: {e}")
            raise

    def exists(self, entity_id: str) -> bool:
        """
        Check if entity exists by ID.

        Args:
            entity_id (str): Entity ID to check

        Returns:
            bool: True if entity exists, False otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            if not entity_id:
                return False

            return self.model.query.get(entity_id) is not None
        except SQLAlchemyError as e:
            self._log_error(
                f"Error checking existence of {
                    self.model.__name__} {entity_id}: {e}")
            raise

    def find_by(self, **kwargs: Any) -> List[T]:
        """
        Find entities by specified criteria.

        Args:
            **kwargs: Filter criteria

        Returns:
            list: List of matching entity instances

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            return self.model.query.filter_by(**kwargs).all()
        except SQLAlchemyError as e:
            self._log_error(
                f"Error finding {
                    self.model.__name__} by criteria {kwargs}: {e}")
            raise

    def find_one_by(self, **kwargs: Any) -> Optional[T]:
        """
        Find one entity by specified criteria.

        Args:
            **kwargs: Filter criteria

        Returns:
            T: Entity instance if found, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            return self.model.query.filter_by(**kwargs).first()
        except SQLAlchemyError as e:
            self._log_error(
                f"Error finding {
                    self.model.__name__} by criteria {kwargs}: {e}")
            raise

    def _validate_entity_data(self, entity_data: Dict[str, Any]) -> None:
        """
        Validate entity data before creation.
        Override in subclasses for specific validation.

        Args:
            entity_data (dict): Entity data to validate

        Raises:
            ValueError: If data is invalid
        """
        if not entity_data:
            raise ValueError("Entity data cannot be empty")

    def _handle_integrity_error(self, error: IntegrityError) -> None:
        """
        Handle integrity errors.
        Override in subclasses for specific error handling.

        Args:
            error (IntegrityError): The integrity error to handle
        """
        error_message = str(error)
        if "UNIQUE constraint failed" in error_message:
            raise ValueError("Entity with this data already exists")
        else:
            raise ValueError(f"Data integrity error: {error_message}")

    def _log_error(self, message: str) -> None:
        """
        Log error messages.
        Override in subclasses for specific logging.

        Args:
            message (str): Error message to log
        """
        # In a production environment, this would use a proper logging system
        print(f"Repository Error: {message}")

    def __repr__(self) -> str:
        """String representation of the repository."""
        return f"<{self.__class__.__name__}(model={self.model.__name__})>"


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
        super().__init__(model)

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
            raise

    def get_all(self) -> List[Any]:
        """
        Get all objects from the database.

        Returns:
            List of all objects
        """
        try:
            return self.model.query.all()
        except Exception as e:
            print(f"Error getting all objects: {e}")
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
            print(f"Error updating object: {e}")
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
            print(f"Error deleting object: {e}")
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
            print(f"Error getting object by attribute: {e}")
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
            print(f"Error getting objects by attributes: {e}")
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
            print(f"Error counting objects: {e}")
            return 0
