"""
User API endpoints for HBnB application.
Handles user-related HTTP requests and responses.
"""

from typing import Dict, Any, Optional
from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import Facade
from .response_utils import APIResponse, handle_exceptions
from .utils import get_current_user, check_ownership_or_admin

facade = Facade()

api = Namespace('users', description='User operations')

register_model = api.model('Register', {
    'email': fields.String(required=True, description='Email is required'),
    'password': fields.String(required=True, description='Password is required'),
    'first_name': fields.String(required=False),
    'last_name': fields.String(required=False)
})

@api.route('/register')
class UserRegister(Resource):
    @api.expect(register_model)
    def post(self):
        args = api.payload
        email = args['email']
        password = args['password']
        first_name = args.get('first_name')
        last_name = args.get('last_name')
        is_admin = False
        if facade.search_users(email):
            return {'error': 'Email already exists'}, 400
        try:
            user = facade.create_user({
                'email': email,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'is_admin': is_admin
            })
            return {'message': 'User created successfully', 'user': user}, 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/search')
class UserSearch(Resource):
    @jwt_required()
    @handle_exceptions
    def get(self):
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
        from flask import request
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

@api.route('/admin/<string:is_admin>')
class UsersByAdminStatus(Resource):
    @jwt_required()
    @handle_exceptions
    def get(self, is_admin):
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
