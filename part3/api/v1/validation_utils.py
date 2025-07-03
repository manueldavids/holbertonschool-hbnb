"""
Validation utilities for API endpoints.
Centralizes common validation logic and patterns.
"""

import re
from typing import Tuple, Optional, Any, Dict
from datetime import datetime


class ValidationUtils:
    """Centralized validation utilities."""
    
    # Regex patterns
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    UUID_REGEX = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str]]:
        """
        Validate email format.
        
        Args:
            email: Email to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email or not isinstance(email, str):
            return False, "Email is required"
        
        email = email.strip()
        if not email:
            return False, "Email cannot be empty"
        
        if not ValidationUtils.EMAIL_REGEX.match(email):
            return False, "Invalid email format"
        
        return True, None
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, Optional[str]]:
        """
        Validate password strength.
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not password or not isinstance(password, str):
            return False, "Password is required"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        return True, None
    
    @staticmethod
    def validate_uuid(uuid_str: str) -> Tuple[bool, Optional[str]]:
        """
        Validate UUID format.
        
        Args:
            uuid_str: UUID string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not uuid_str or not isinstance(uuid_str, str):
            return False, "UUID is required"
        
        if not ValidationUtils.UUID_REGEX.match(uuid_str):
            return False, "Invalid UUID format"
        
        return True, None
    
    @staticmethod
    def validate_string_field(value: Any, field_name: str, 
                            min_length: int = 1, max_length: Optional[int] = None) -> Tuple[bool, Optional[str]]:
        """
        Validate string field with length constraints.
        
        Args:
            value: Value to validate
            field_name: Name of the field for error messages
            min_length: Minimum length required
            max_length: Maximum length allowed
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(value, str):
            return False, f"{field_name} must be a string"
        
        if len(value.strip()) < min_length:
            return False, f"{field_name} must be at least {min_length} characters long"
        
        if max_length and len(value) > max_length:
            return False, f"{field_name} must be no more than {max_length} characters long"
        
        return True, None
    
    @staticmethod
    def validate_integer_field(value: Any, field_name: str, 
                             min_value: Optional[int] = None, 
                             max_value: Optional[int] = None) -> Tuple[bool, Optional[str]]:
        """
        Validate integer field with range constraints.
        
        Args:
            value: Value to validate
            field_name: Name of the field for error messages
            min_value: Minimum value allowed
            max_value: Maximum value allowed
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            int_value = int(value)
        except (ValueError, TypeError):
            return False, f"{field_name} must be an integer"
        
        if min_value is not None and int_value < min_value:
            return False, f"{field_name} must be at least {min_value}"
        
        if max_value is not None and int_value > max_value:
            return False, f"{field_name} must be no more than {max_value}"
        
        return True, None
    
    @staticmethod
    def validate_float_field(value: Any, field_name: str,
                           min_value: Optional[float] = None,
                           max_value: Optional[float] = None) -> Tuple[bool, Optional[str]]:
        """
        Validate float field with range constraints.
        
        Args:
            value: Value to validate
            field_name: Name of the field for error messages
            min_value: Minimum value allowed
            max_value: Maximum value allowed
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            float_value = float(value)
        except (ValueError, TypeError):
            return False, f"{field_name} must be a number"
        
        if min_value is not None and float_value < min_value:
            return False, f"{field_name} must be at least {min_value}"
        
        if max_value is not None and float_value > max_value:
            return False, f"{field_name} must be no more than {max_value}"
        
        return True, None
    
    @staticmethod
    def validate_boolean_field(value: Any, field_name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate boolean field.
        
        Args:
            value: Value to validate
            field_name: Name of the field for error messages
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(value, bool):
            return False, f"{field_name} must be a boolean"
        
        return True, None
    
    @staticmethod
    def validate_date_field(value: Any, field_name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate date field.
        
        Args:
            value: Value to validate
            field_name: Name of the field for error messages
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(value, str):
            return False, f"{field_name} must be a string"
        
        try:
            datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError:
            return False, f"{field_name} must be a valid ISO date format"
        
        return True, None
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], 
                               required_fields: list) -> Tuple[bool, Optional[str]]:
        """
        Validate that required fields are present in data.
        
        Args:
            data: Data dictionary to validate
            required_fields: List of required field names
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not data:
            return False, "No data provided"
        
        for field in required_fields:
            if field not in data or data[field] is None:
                return False, f"Field '{field}' is required"
        
        return True, None
    
    @staticmethod
    def validate_user_data(user_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate user data for creation/update.
        
        Args:
            user_data: User data dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate required fields
        required_fields = ['email', 'password']
        is_valid, error = ValidationUtils.validate_required_fields(user_data, required_fields)
        if not is_valid:
            return False, error
        
        # Validate email
        is_valid, error = ValidationUtils.validate_email(user_data['email'])
        if not is_valid:
            return False, error
        
        # Validate password
        is_valid, error = ValidationUtils.validate_password(user_data['password'])
        if not is_valid:
            return False, error
        
        # Validate optional fields
        if 'first_name' in user_data:
            is_valid, error = ValidationUtils.validate_string_field(
                user_data['first_name'], 'first_name', max_length=100)
            if not is_valid:
                return False, error
        
        if 'last_name' in user_data:
            is_valid, error = ValidationUtils.validate_string_field(
                user_data['last_name'], 'last_name', max_length=100)
            if not is_valid:
                return False, error
        
        if 'is_admin' in user_data:
            is_valid, error = ValidationUtils.validate_boolean_field(
                user_data['is_admin'], 'is_admin')
            if not is_valid:
                return False, error
        
        return True, None
    
    @staticmethod
    def validate_place_data(place_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate place data for creation/update.
        
        Args:
            place_data: Place data dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate required fields
        required_fields = ['name', 'description', 'latitude', 'longitude']
        is_valid, error = ValidationUtils.validate_required_fields(place_data, required_fields)
        if not is_valid:
            return False, error
        
        # Validate name
        is_valid, error = ValidationUtils.validate_string_field(
            place_data['name'], 'name', max_length=255)
        if not is_valid:
            return False, error
        
        # Validate description
        is_valid, error = ValidationUtils.validate_string_field(
            place_data['description'], 'description', max_length=1000)
        if not is_valid:
            return False, error
        
        # Validate coordinates
        is_valid, error = ValidationUtils.validate_float_field(
            place_data['latitude'], 'latitude', -90, 90)
        if not is_valid:
            return False, error
        
        is_valid, error = ValidationUtils.validate_float_field(
            place_data['longitude'], 'longitude', -180, 180)
        if not is_valid:
            return False, error
        
        # Validate optional fields
        if 'price_per_night' in place_data:
            is_valid, error = ValidationUtils.validate_float_field(
                place_data['price_per_night'], 'price_per_night', 0)
            if not is_valid:
                return False, error
        
        if 'max_guests' in place_data:
            is_valid, error = ValidationUtils.validate_integer_field(
                place_data['max_guests'], 'max_guests', 1)
            if not is_valid:
                return False, error
        
        return True, None 