"""
User API endpoints for HBnB application.
Handles user-related HTTP requests and responses.
"""

from typing import Dict, Any, Optional
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import Facade
from app.models.user import User

# Create blueprint
users_bp = Blueprint('users', __name__)

# Initialize facade
facade = Facade()


@users_bp.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user.

    Expected JSON payload:
    {
        "email": "user@example.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe",
        "is_admin": false
    }

    Returns:
        JSON response with user data or error message
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate required fields
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Field "{field}" is required'}), 400

        # Create user
        user_data = facade.create_user(data)

        return jsonify({
            'message': 'User created successfully',
            'user': user_data
        }), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error creating user: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@users_bp.route('/users/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id: str):
    """
    Get user by ID.

    Args:
        user_id (str): User ID to retrieve

    Returns:
        JSON response with user data or error message
    """
    try:
        # Get current user from JWT
        current_user_id = get_jwt_identity()

        # Check if user is requesting their own data or is admin
        if current_user_id != user_id:
            # Check if current user is admin
            current_user = facade.get_user(current_user_id)
            if not current_user or not current_user.get('is_admin'):
                return jsonify({'error': 'Unauthorized access'}), 403

        # Get user data
        user_data = facade.get_user(user_id)
        if not user_data:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'message': 'User retrieved successfully',
            'user': user_data
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error getting user {user_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    """
    Get all users with optional pagination.

    Query parameters:
        limit (int, optional): Maximum number of users to return
        offset (int, optional): Number of users to skip

    Returns:
        JSON response with list of users or error message
    """
    try:
        # Get current user from JWT
        current_user_id = get_jwt_identity()

        # Check if current user is admin
        current_user = facade.get_user(current_user_id)
        if not current_user or not current_user.get('is_admin'):
            return jsonify({'error': 'Admin access required'}), 403

        # Get pagination parameters
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', 0, type=int)

        # Validate pagination parameters
        if limit is not None and limit < 0:
            return jsonify({'error': 'Limit must be positive'}), 400
        if offset < 0:
            return jsonify({'error': 'Offset must be non-negative'}), 400

        # Get users
        users = facade.get_all_users(limit=limit, offset=offset)

        return jsonify({
            'message': 'Users retrieved successfully',
            'users': users,
            'count': len(users)
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error getting all users: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@users_bp.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id: str):
    """
    Update user information.

    Args:
        user_id (str): User ID to update

    Expected JSON payload:
    {
        "email": "newemail@example.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "is_admin": true
    }

    Returns:
        JSON response with updated user data or error message
    """
    try:
        # Get current user from JWT
        current_user_id = get_jwt_identity()

        # Check if user is updating their own data or is admin
        if current_user_id != user_id:
            # Check if current user is admin
            current_user = facade.get_user(current_user_id)
            if not current_user or not current_user.get('is_admin'):
                return jsonify({'error': 'Unauthorized access'}), 403

        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Remove password from update data (use separate endpoint for password
        # updates)
        data.pop('password', None)

        # Update user
        user_data = facade.update_user(user_id, data)
        if not user_data:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'message': 'User updated successfully',
            'user': user_data
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error updating user {user_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@users_bp.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id: str):
    """
    Delete a user.

    Args:
        user_id (str): User ID to delete

    Returns:
        JSON response with success or error message
    """
    try:
        # Get current user from JWT
        current_user_id = get_jwt_identity()

        # Check if user is deleting their own account or is admin
        if current_user_id != user_id:
            # Check if current user is admin
            current_user = facade.get_user(current_user_id)
            if not current_user or not current_user.get('is_admin'):
                return jsonify({'error': 'Unauthorized access'}), 403

        # Delete user
        success = facade.delete_user(user_id)
        if not success:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'message': 'User deleted successfully'
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error deleting user {user_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@users_bp.route('/users/search', methods=['GET'])
@jwt_required()
def search_users():
    """
    Search users by email, first name, or last name.

    Query parameters:
        q (str): Search term
        limit (int, optional): Maximum number of results

    Returns:
        JSON response with matching users or error message
    """
    try:
        # Get current user from JWT
        current_user_id = get_jwt_identity()

        # Check if current user is admin
        current_user = facade.get_user(current_user_id)
        if not current_user or not current_user.get('is_admin'):
            return jsonify({'error': 'Admin access required'}), 403

        # Get search parameters
        search_term = request.args.get('q')
        limit = request.args.get('limit', type=int)

        if not search_term:
            return jsonify({'error': 'Search term is required'}), 400

        # Validate limit parameter
        if limit is not None and limit < 0:
            return jsonify({'error': 'Limit must be positive'}), 400

        # Search users
        users = facade.search_users(search_term, limit=limit)

        return jsonify({
            'message': 'Search completed successfully',
            'users': users,
            'count': len(users),
            'search_term': search_term
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error searching users: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@users_bp.route('/users/admin/<is_admin>', methods=['GET'])
@jwt_required()
def get_users_by_admin_status(is_admin: str):
    """
    Get users by admin status.

    Args:
        is_admin (str): Admin status filter ('true' or 'false')

    Returns:
        JSON response with filtered users or error message
    """
    try:
        # Get current user from JWT
        current_user_id = get_jwt_identity()

        # Check if current user is admin
        current_user = facade.get_user(current_user_id)
        if not current_user or not current_user.get('is_admin'):
            return jsonify({'error': 'Admin access required'}), 403

        # Validate admin status parameter
        if is_admin.lower() not in ['true', 'false']:
            return jsonify(
                {'error': 'Admin status must be "true" or "false"'}), 400

        is_admin_bool = is_admin.lower() == 'true'

        # Get users by admin status
        users = facade.get_users_by_admin_status(is_admin_bool)

        return jsonify({
            'message': 'Users retrieved successfully',
            'users': users,
            'count': len(users),
            'is_admin': is_admin_bool
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error getting users by admin status: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@users_bp.route('/users/<user_id>/password', methods=['PUT'])
@jwt_required()
def update_user_password(user_id: str):
    """
    Update user password.

    Args:
        user_id (str): User ID to update password for

    Expected JSON payload:
    {
        "new_password": "newpassword123"
    }

    Returns:
        JSON response with success or error message
    """
    try:
        # Get current user from JWT
        current_user_id = get_jwt_identity()

        # Check if user is updating their own password or is admin
        if current_user_id != user_id:
            # Check if current user is admin
            current_user = facade.get_user(current_user_id)
            if not current_user or not current_user.get('is_admin'):
                return jsonify({'error': 'Unauthorized access'}), 403

        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        new_password = data.get('new_password')
        if not new_password:
            return jsonify({'error': 'New password is required'}), 400

        # Validate password strength
        if len(new_password) < 6:
            return jsonify(
                {'error': 'Password must be at least 6 characters long'}), 400

        # Update password
        success = facade.update_user_password(user_id, new_password)
        if not success:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'message': 'Password updated successfully'
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(
            f"Error updating password for user {user_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@users_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Resource not found'}), 404


@users_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500
