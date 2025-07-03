"""
Response utilities for API endpoints.
Centralizes common response patterns and error handling.
"""

from typing import Dict, Any, Optional, Union, Tuple
from flask import jsonify, current_app
from http import HTTPStatus


class APIResponse:
    """Centralized API response handling."""
    
    @staticmethod
    def success(data: Any = None, message: str = "Success", 
                status_code: int = 200) -> Tuple[Dict[str, Any], int]:
        """
        Create a successful API response.
        
        Args:
            data: Response data
            message: Success message
            status_code: HTTP status code
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        response = {
            'message': message,
            'status': 'success'
        }
        
        if data is not None:
            if isinstance(data, list):
                response['data'] = data
                response['count'] = len(data)
            elif isinstance(data, dict):
                response.update(data)
            else:
                response['data'] = data
                
        return jsonify(response), status_code
    
    @staticmethod
    def error(message: str, status_code: int = 400, 
              details: Optional[str] = None) -> Tuple[Dict[str, Any], int]:
        """
        Create an error API response.
        
        Args:
            message: Error message
            status_code: HTTP status code
            details: Additional error details
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        response = {
            'error': message,
            'status': 'error'
        }
        
        if details:
            response['details'] = details
            
        return jsonify(response), status_code
    
    @staticmethod
    def not_found(resource: str = "Resource") -> Tuple[Dict[str, Any], int]:
        """Create a 404 not found response."""
        return APIResponse.error(f"{resource} not found", 404)
    
    @staticmethod
    def unauthorized(message: str = "Unauthorized access") -> Tuple[Dict[str, Any], int]:
        """Create a 401 unauthorized response."""
        return APIResponse.error(message, 401)
    
    @staticmethod
    def forbidden(message: str = "Forbidden - access denied") -> Tuple[Dict[str, Any], int]:
        """Create a 403 forbidden response."""
        return APIResponse.error(message, 403)
    
    @staticmethod
    def bad_request(message: str = "Bad request", 
                   details: Optional[str] = None) -> Tuple[Dict[str, Any], int]:
        """Create a 400 bad request response."""
        return APIResponse.error(message, 400, details)
    
    @staticmethod
    def internal_error(message: str = "Internal server error", 
                      details: Optional[str] = None) -> Tuple[Dict[str, Any], int]:
        """Create a 500 internal server error response."""
        return APIResponse.error(message, 500, details)
    
    @staticmethod
    def validation_error(field: str, message: str) -> Tuple[Dict[str, Any], int]:
        """Create a validation error response."""
        return APIResponse.bad_request(f"Field '{field}': {message}")
    
    @staticmethod
    def created(data: Any = None, message: str = "Created successfully") -> Tuple[Dict[str, Any], int]:
        """Create a 201 created response."""
        return APIResponse.success(data, message, 201)


def handle_exceptions(func):
    """
    Decorator to handle exceptions consistently across API endpoints.
    
    Args:
        func: Function to decorate
        
    Returns:
        function: Decorated function
    """
    from functools import wraps
    
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            current_app.logger.warning(f"Validation error in {func.__name__}: {e}")
            return APIResponse.bad_request(str(e))
        except Exception as e:
            current_app.logger.error(f"Error in {func.__name__}: {e}")
            return APIResponse.internal_error()
    
    return decorated_function


def validate_required_fields(data: Dict[str, Any], 
                           required_fields: list) -> Optional[Tuple[Dict[str, Any], int]]:
    """
    Validate that required fields are present in request data.
    
    Args:
        data: Request data dictionary
        required_fields: List of required field names
        
    Returns:
        Error response tuple if validation fails, None if valid
    """
    if not data:
        return APIResponse.bad_request("No data provided")
    
    for field in required_fields:
        if field not in data or not data[field]:
            return APIResponse.validation_error(field, "is required")
    
    return None


def validate_pagination_params(limit: Optional[int], offset: int) -> Optional[Tuple[Dict[str, Any], int]]:
    """
    Validate pagination parameters.
    
    Args:
        limit: Maximum number of items
        offset: Number of items to skip
        
    Returns:
        Error response tuple if validation fails, None if valid
    """
    if limit is not None and limit < 0:
        return APIResponse.bad_request("Limit must be positive")
    
    if offset < 0:
        return APIResponse.bad_request("Offset must be non-negative")
    
    return None 