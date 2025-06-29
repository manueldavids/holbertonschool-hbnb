"""
User management endpoints for the HBnB API.
Handles user registration and user data operations.
"""

import re
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy.exc import IntegrityError
from app.models.user import User, db

api = Namespace('users', description='User management operations')

# Email validation regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# Model for user registration input validation
user_registration_model = api.model('UserRegistration', {
    'email': fields.String(
        required=True,
        description='User email address',
        example='user@example.com'
    ),
    'password': fields.String(
        required=True,
        description='User password (minimum 6 characters)',
        example='securepassword123'
    ),
    'first_name': fields.String(
        description='User first name',
        example='John'
    ),
    'last_name': fields.String(
        description='User last name',
        example='Doe'
    ),
    'is_admin': fields.Boolean(
        description='Admin privileges flag',
        default=False
    )
})

# Model for user response (password excluded for security)
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'email': fields.String(description='User email address'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'is_admin': fields.Boolean(description='Admin privileges flag'),
    'created_at': fields.String(description='User creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

# Model for user update input validation
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'is_admin': fields.Boolean(description='Admin privileges flag')
})

# Model for error responses
error_model = api.model('Error', {
    'error': fields.String(description='Error message'),
    'details': fields.String(
        description='Additional error details',
        required=False
    )
})


def validate_email(email):
    """
    Validate email format.
    
    Args:
        email (str): Email to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


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


@api.route('/')
class UserRegistration(Resource):
    @api.expect(user_registration_model)
    @api.response(201, 'User created successfully', user_response_model)
    @api.response(400, 'Bad request - validation error', error_model)
    @api.response(409, 'User already exists', error_model)
    @api.response(500, 'Internal server error', error_model)
    def post(self):
        """
        Register a new user with password hashing.

        This endpoint creates a new user account with a securely hashed
        password. The password is never stored in plain text and is not
        returned in responses.
        """
        try:
            # Get user data from request payload
            user_data = api.payload

            # Validate required fields
            if not user_data:
                return {
                    'error': 'Request body is required'
                }, 400

            email = user_data.get('email')
            password = user_data.get('password')

            if not email or not password:
                return {
                    'error': 'Email and password are required'
                }, 400

            # Validate email format
            if not validate_email(email):
                return {
                    'error': 'Invalid email format'
                }, 400

            # Validate password strength
            is_valid_password, password_error = validate_password(password)
            if not is_valid_password:
                return {
                    'error': password_error
                }, 400

            # Extract optional fields
            first_name = user_data.get('first_name')
            last_name = user_data.get('last_name')
            is_admin = user_data.get('is_admin', False)

            # Check if user already exists
            existing_user = User.get_by_email(email)
            if existing_user:
                return {
                    'error': 'User with this email already exists'
                }, 409

            # Create new user with password hashing
            try:
                new_user = User.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    is_admin=is_admin
                )
            except ValueError as e:
                return {
                    'error': str(e)
                }, 400

            # Save to database
            try:
                db.session.add(new_user)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return {
                    'error': 'User with this email already exists'
                }, 409

            # Return user data (password excluded)
            return new_user.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            return {
                'error': 'User registration failed',
                'details': str(e)
            }, 500


@api.route('/<string:user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.response(200, 'User retrieved successfully', user_response_model)
    @api.response(404, 'User not found', error_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(500, 'Internal server error', error_model)
    def get(self, user_id):
        """
        Get user information by ID.

        This endpoint returns user data excluding the password hash for
        security. Users can only access their own data, unless they are
        admin.
        """
        try:
            # Validate user_id
            if not user_id:
                return {
                    'error': 'User ID is required'
                }, 400

            # Get current user identity
            current_user_id = get_jwt_identity()
            current_claims = get_jwt()
            is_admin = current_claims.get('is_admin', False)

            # Users can only access their own data, unless they are admin
            if current_user_id != user_id and not is_admin:
                return {
                    'error': 'Unauthorized - can only access own user data'
                }, 401

            # Get user from database
            user = User.get_by_id(user_id)
            if not user:
                return {
                    'error': 'User not found'
                }, 404

            # Return user data (password excluded)
            return user.to_dict(), 200

        except Exception as e:
            return {
                'error': 'Failed to retrieve user',
                'details': str(e)
            }, 500

    @jwt_required()
    @api.expect(user_update_model)
    @api.response(200, 'User updated successfully', user_response_model)
    @api.response(400, 'Bad request', error_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(404, 'User not found', error_model)
    @api.response(500, 'Internal server error', error_model)
    def put(self, user_id):
        """
        Update user details (excluding email and password).

        This endpoint allows users to update their own details.
        Users can only update their own data, unless they are admin.
        Email and password cannot be updated through this endpoint.
        """
        try:
            # Validate user_id
            if not user_id:
                return {
                    'error': 'User ID is required'
                }, 400

            # Get current user identity
            current_user_id = get_jwt_identity()
            current_claims = get_jwt()
            is_admin = current_claims.get('is_admin', False)

            # Users can only update their own data, unless they are admin
            if current_user_id != user_id and not is_admin:
                return {
                    'error': 'Unauthorized - can only update own user data'
                }, 401

            # Get user from database
            user = User.get_by_id(user_id)
            if not user:
                return {
                    'error': 'User not found'
                }, 404

            # Get update data from request payload
            update_data = api.payload
            if not update_data:
                return {
                    'error': 'Update data is required'
                }, 400

            # Remove email and password from update data (not allowed)
            if 'email' in update_data:
                del update_data['email']
            if 'password' in update_data:
                del update_data['password']

            # Update user fields
            for field, value in update_data.items():
                if hasattr(user, field) and value is not None:
                    setattr(user, field, value)

            # Save changes to database
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return {
                    'error': 'Failed to update user data'
                }, 500

            # Return updated user data (password excluded)
            return user.to_dict(), 200

        except Exception as e:
            db.session.rollback()
            return {
                'error': 'Failed to update user',
                'details': str(e)
            }, 500


@api.route('/me')
class CurrentUser(Resource):
    @jwt_required()
    @api.response(200, 'Current user retrieved successfully', 
                 user_response_model)
    @api.response(404, 'User not found', error_model)
    @api.response(500, 'Internal server error', error_model)
    def get(self):
        """
        Get current user information.

        This endpoint returns the current authenticated user's data.
        """
        try:
            # Get current user identity
            current_user_id = get_jwt_identity()

            # Get user from database
            user = User.get_by_id(current_user_id)
            if not user:
                return {
                    'error': 'User not found'
                }, 404

            # Return user data (password excluded)
            return user.to_dict(), 200

        except Exception as e:
            return {
                'error': 'Failed to retrieve current user',
                'details': str(e)
            }, 500


@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.response(200, 'Users retrieved successfully')
    @api.response(401, 'Unauthorized', error_model)
    @api.response(500, 'Internal server error', error_model)
    def get(self):
        """
        Get all users (admin only).

        This endpoint returns a list of all users, excluding password
        hashes. Only admin users can access this endpoint.
        """
        try:
            # Get current user claims
            current_claims = get_jwt()
            is_admin = current_claims.get('is_admin', False)

            # Only admin users can list all users
            if not is_admin:
                return {
                    'error': 'Unauthorized - admin access required'
                }, 401

            # Get all users with pagination
            users = User.get_all_users()
            
            # Return user data (passwords excluded)
            return {
                'users': [user.to_dict() for user in users],
                'total': len(users)
            }, 200

        except Exception as e:
            return {
                'error': 'Failed to retrieve users',
                'details': str(e)
            }, 500
