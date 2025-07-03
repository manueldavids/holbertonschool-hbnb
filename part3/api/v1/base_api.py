"""
Base API class for common CRUD operations.
Provides reusable patterns for API endpoints.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from .response_utils import APIResponse, handle_exceptions
from .validation_utils import ValidationUtils
from .utils import get_current_user, require_admin, check_ownership_or_admin


class BaseAPI(ABC):
    """
    Base class for API endpoints with common CRUD operations.
    Reduces code duplication across endpoint modules.
    """
    
    def __init__(self, blueprint: Blueprint, facade, entity_name: str):
        """
        Initialize base API.
        
        Args:
            blueprint: Flask blueprint
            facade: Business logic facade
            entity_name: Name of the entity (e.g., 'user', 'place')
        """
        self.blueprint = blueprint
        self.facade = facade
        self.entity_name = entity_name
        self._register_routes()
    
    def _register_routes(self):
        """Register common CRUD routes."""
        # Create
        self.blueprint.add_url_rule(
            f'/{self.entity_name}s',
            f'create_{self.entity_name}',
            self.create_entity,
            methods=['POST']
        )
        
        # Read (single)
        self.blueprint.add_url_rule(
            f'/{self.entity_name}s/<entity_id>',
            f'get_{self.entity_name}',
            self.get_entity,
            methods=['GET']
        )
        
        # Read (all)
        self.blueprint.add_url_rule(
            f'/{self.entity_name}s',
            f'get_all_{self.entity_name}s',
            self.get_all_entities,
            methods=['GET']
        )
        
        # Update
        self.blueprint.add_url_rule(
            f'/{self.entity_name}s/<entity_id>',
            f'update_{self.entity_name}',
            self.update_entity,
            methods=['PUT']
        )
        
        # Delete
        self.blueprint.add_url_rule(
            f'/{self.entity_name}s/<entity_id>',
            f'delete_{self.entity_name}',
            self.delete_entity,
            methods=['DELETE']
        )
    
    @handle_exceptions
    def create_entity(self, entity_id: str = None) -> Tuple[Dict[str, Any], int]:
        """
        Create a new entity.
        
        Args:
            entity_id: Not used for creation
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        data = request.get_json()
        if not data:
            return APIResponse.bad_request("No data provided")
        
        # Validate data
        is_valid, error = self._validate_entity_data(data)
        if not is_valid:
            return APIResponse.bad_request(error)
        
        # Create entity
        entity_data = self._create_entity_logic(data)
        
        return APIResponse.created(
            {self.entity_name: entity_data},
            f"{self.entity_name.title()} created successfully"
        )
    
    @jwt_required()
    @handle_exceptions
    def get_entity(self, entity_id: str) -> Tuple[Dict[str, Any], int]:
        """
        Get entity by ID.
        
        Args:
            entity_id: Entity ID to retrieve
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        # Validate UUID
        is_valid, error = ValidationUtils.validate_uuid(entity_id)
        if not is_valid:
            return APIResponse.bad_request(error)
        
        # Check permissions
        permission_check = self._check_get_permissions(entity_id)
        if permission_check:
            return permission_check
        
        # Get entity
        entity_data = self._get_entity_logic(entity_id)
        if not entity_data:
            return APIResponse.not_found(self.entity_name.title())
        
        return APIResponse.success({
            self.entity_name: entity_data
        }, f"{self.entity_name.title()} retrieved successfully")
    
    @jwt_required()
    @handle_exceptions
    def get_all_entities(self) -> Tuple[Dict[str, Any], int]:
        """
        Get all entities with optional pagination.
        
        Returns:
            Tuple of (response_dict, status_code)
        """
        # Check permissions
        permission_check = self._check_list_permissions()
        if permission_check:
            return permission_check
        
        # Get pagination parameters
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Validate pagination
        pagination_error = ValidationUtils.validate_pagination_params(limit, offset)
        if pagination_error:
            return pagination_error
        
        # Get entities
        entities = self._get_all_entities_logic(limit, offset)
        
        return APIResponse.success({
            f"{self.entity_name}s": entities,
            'count': len(entities)
        }, f"{self.entity_name.title()}s retrieved successfully")
    
    @jwt_required()
    @handle_exceptions
    def update_entity(self, entity_id: str) -> Tuple[Dict[str, Any], int]:
        """
        Update entity.
        
        Args:
            entity_id: Entity ID to update
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        # Validate UUID
        is_valid, error = ValidationUtils.validate_uuid(entity_id)
        if not is_valid:
            return APIResponse.bad_request(error)
        
        # Check permissions
        permission_check = self._check_update_permissions(entity_id)
        if permission_check:
            return permission_check
        
        data = request.get_json()
        if not data:
            return APIResponse.bad_request("No data provided")
        
        # Validate data
        is_valid, error = self._validate_update_data(data)
        if not is_valid:
            return APIResponse.bad_request(error)
        
        # Update entity
        entity_data = self._update_entity_logic(entity_id, data)
        if not entity_data:
            return APIResponse.not_found(self.entity_name.title())
        
        return APIResponse.success({
            self.entity_name: entity_data
        }, f"{self.entity_name.title()} updated successfully")
    
    @jwt_required()
    @handle_exceptions
    def delete_entity(self, entity_id: str) -> Tuple[Dict[str, Any], int]:
        """
        Delete entity.
        
        Args:
            entity_id: Entity ID to delete
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        # Validate UUID
        is_valid, error = ValidationUtils.validate_uuid(entity_id)
        if not is_valid:
            return APIResponse.bad_request(error)
        
        # Check permissions
        permission_check = self._check_delete_permissions(entity_id)
        if permission_check:
            return permission_check
        
        # Delete entity
        success = self._delete_entity_logic(entity_id)
        if not success:
            return APIResponse.not_found(self.entity_name.title())
        
        return APIResponse.success(
            message=f"{self.entity_name.title()} deleted successfully"
        )
    
    # Abstract methods that must be implemented by subclasses
    @abstractmethod
    def _validate_entity_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate entity data for creation."""
        pass
    
    @abstractmethod
    def _validate_update_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate entity data for update."""
        pass
    
    @abstractmethod
    def _create_entity_logic(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create entity logic."""
        pass
    
    @abstractmethod
    def _get_entity_logic(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get entity logic."""
        pass
    
    @abstractmethod
    def _get_all_entities_logic(self, limit: Optional[int], 
                               offset: int) -> List[Dict[str, Any]]:
        """Get all entities logic."""
        pass
    
    @abstractmethod
    def _update_entity_logic(self, entity_id: str, 
                           data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update entity logic."""
        pass
    
    @abstractmethod
    def _delete_entity_logic(self, entity_id: str) -> bool:
        """Delete entity logic."""
        pass
    
    # Permission check methods (can be overridden by subclasses)
    def _check_get_permissions(self, entity_id: str) -> Optional[Tuple[Dict[str, Any], int]]:
        """Check permissions for getting entity. Override if needed."""
        return None
    
    def _check_list_permissions(self) -> Optional[Tuple[Dict[str, Any], int]]:
        """Check permissions for listing entities. Override if needed."""
        return None
    
    def _check_update_permissions(self, entity_id: str) -> Optional[Tuple[Dict[str, Any], int]]:
        """Check permissions for updating entity. Override if needed."""
        return None
    
    def _check_delete_permissions(self, entity_id: str) -> Optional[Tuple[Dict[str, Any], int]]:
        """Check permissions for deleting entity. Override if needed."""
        return None


class UserAPI(BaseAPI):
    """User-specific API implementation."""
    
    def __init__(self, blueprint: Blueprint, facade):
        super().__init__(blueprint, facade, 'user')
    
    def _validate_entity_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        return ValidationUtils.validate_user_data(data)
    
    def _validate_update_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        # For updates, password is optional
        if 'password' in data:
            is_valid, error = ValidationUtils.validate_password(data['password'])
            if not is_valid:
                return False, error
        
        if 'email' in data:
            is_valid, error = ValidationUtils.validate_email(data['email'])
            if not is_valid:
                return False, error
        
        return True, None
    
    def _create_entity_logic(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.facade.create_user(data)
    
    def _get_entity_logic(self, entity_id: str) -> Optional[Dict[str, Any]]:
        return self.facade.get_user(entity_id)
    
    def _get_all_entities_logic(self, limit: Optional[int], 
                               offset: int) -> List[Dict[str, Any]]:
        return self.facade.get_all_users(limit=limit, offset=offset)
    
    def _update_entity_logic(self, entity_id: str, 
                           data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.facade.update_user(entity_id, data)
    
    def _delete_entity_logic(self, entity_id: str) -> bool:
        return self.facade.delete_user(entity_id)
    
    def _check_get_permissions(self, entity_id: str) -> Optional[Tuple[Dict[str, Any], int]]:
        current_user_id = get_jwt_identity()
        if current_user_id != entity_id and not check_ownership_or_admin(entity_id, current_user_id):
            return APIResponse.forbidden("Unauthorized access")
        return None
    
    def _check_list_permissions(self) -> Optional[Tuple[Dict[str, Any], int]]:
        if not get_current_user() or not check_ownership_or_admin(None, get_jwt_identity()):
            return APIResponse.forbidden("Admin access required")
        return None
    
    def _check_update_permissions(self, entity_id: str) -> Optional[Tuple[Dict[str, Any], int]]:
        current_user_id = get_jwt_identity()
        if current_user_id != entity_id and not check_ownership_or_admin(entity_id, current_user_id):
            return APIResponse.forbidden("Unauthorized access")
        return None
    
    def _check_delete_permissions(self, entity_id: str) -> Optional[Tuple[Dict[str, Any], int]]:
        current_user_id = get_jwt_identity()
        if current_user_id != entity_id and not check_ownership_or_admin(entity_id, current_user_id):
            return APIResponse.forbidden("Unauthorized access")
        return None 