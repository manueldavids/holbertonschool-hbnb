"""
Utility functions for API endpoints.
Centralizes common authentication and authorization logic.
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt
from app.models.user import User


def get_current_user():
    """
    Get current authenticated user.
    
    Returns:
        User: Current user instance or None if not authenticated
    """
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return None
        return User.get_by_id(current_user_id)
    except Exception:
        return None


def get_current_admin_user():
    """
    Get current authenticated user and verify admin privileges.
    
    Returns:
        User: Current admin user instance or None if not admin
    """
    try:
        current_user_id = get_jwt_identity()
        current_claims = get_jwt()
        is_admin = current_claims.get('is_admin', False)
        
        if not is_admin:
            return None
            
        return User.get_by_id(current_user_id)
    except Exception:
        return None


def is_admin_user():
    """
    Check if current user has admin privileges.
    
    Returns:
        bool: True if user is admin, False otherwise
    """
    try:
        current_claims = get_jwt()
        return current_claims.get('is_admin', False)
    except Exception:
        return False


def require_admin(f):
    """
    Decorator to require admin privileges.
    
    Args:
        f: Function to decorate
        
    Returns:
        function: Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_user = get_current_admin_user()
        if not admin_user:
            return jsonify({
                'error': 'Forbidden - admin access required'
            }), 403
        return f(*args, **kwargs)
    return decorated_function


def check_ownership_or_admin(resource_owner_id, user_id):
    """
    Check if user owns the resource or is admin.
    
    Args:
        resource_owner_id (str): ID of the resource owner
        user_id (str): ID of the current user
        
    Returns:
        bool: True if user owns resource or is admin, False otherwise
    """
    return (str(resource_owner_id) == str(user_id) or is_admin_user())


def validate_email(email):
    """
    Validate email format.
    
    Args:
        email (str): Email to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    import re
    if not email or not isinstance(email, str):
        return False
    email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(email_regex.match(email.strip()))


def validate_password(password):
    """
    Validate password strength.
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not password or not isinstance(password, str):
        return False, "Password is required"
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, None


def handle_database_error(func):
    """
    Decorator to handle database errors consistently.
    
    Args:
        func: Function to decorate
        
    Returns:
        function: Decorated function
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'error': 'Internal server error',
                'details': str(e)
            }), 500
    return decorated_function 