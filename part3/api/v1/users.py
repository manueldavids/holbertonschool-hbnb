"""
User API endpoints for HBnB application.
Handles user-related HTTP requests and responses.
"""

from typing import Dict, Any, Optional
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import Facade
from .base_api import UserAPI
from .response_utils import APIResponse, handle_exceptions
from .validation_utils import ValidationUtils
from .utils import get_current_user, require_admin, check_ownership_or_admin

# Create blueprint
users_bp = Blueprint('users', __name__)

# Initialize facade and base API
facade = Facade()
user_api = UserAPI(users_bp, facade)


@users_bp.route('/users/search', methods=['GET'])
@jwt_required()
@handle_exceptions
def search_users():
    """
    Search users by email, first name, or last name.

    Query parameters:
        q (str): Search term
        limit (int, optional): Maximum number of results

    Returns:
        JSON response with matching users or error message
    """
    # Check admin permissions
    if not get_current_user() or not check_ownership_or_admin(
        None, get_jwt_identity()
    ):
        return APIResponse.forbidden("Admin access required")

    # Get search parameters
    search_term = request.args.get('q')
    limit = request.args.get('limit', type=int)

    if not search_term:
        return APIResponse.bad_request("Search term is required")

    # Validate limit parameter
    if limit is not None and limit < 0:
        return APIResponse.bad_request("Limit must be positive")

    # Search users
    users = facade.search_users(search_term, limit=limit)

    return APIResponse.success(
        {
            "users": users,
            "count": len(users),
            "search_term": search_term
        },
        "Search completed successfully"
    )


@users_bp.route('/users/admin/<is_admin>', methods=['GET'])
@jwt_required()
@handle_exceptions
def get_users_by_admin_status(is_admin: str):
    """
    Get users by admin status.

    Args:
        is_admin (str): Admin status filter ('true' or 'false')

    Returns:
        JSON response with filtered users or error message
    """
    # Check admin permissions
    if not get_current_user() or not check_ownership_or_admin(
        None, get_jwt_identity()
    ):
        return APIResponse.forbidden("Admin access required")

    # Validate admin status parameter
    if is_admin.lower() not in ['true', 'false']:
        return APIResponse.bad_request(
            'Admin status must be "true" or "false"'
        )

    is_admin_bool = is_admin.lower() == 'true'

    # Get users by admin status
    users = facade.get_users_by_admin_status(is_admin_bool)

    return APIResponse.success(
        {
            "users": users,
            "count": len(users),
            "is_admin": is_admin_bool
        },
        "Users retrieved successfully"
    )


@users_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return APIResponse.not_found()


@users_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return APIResponse.internal_error()
