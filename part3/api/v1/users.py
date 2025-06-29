"""
User management endpoints for the HBnB API.
Handles user registration and user data operations.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User, db

api = Namespace('users', description='User management operations')

# Model for user registration input validation
user_registration_model = api.model('UserRegistration', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'is_admin': fields.Boolean(description='Admin privileges flag')
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


@api.route('/')
class UserRegistration(Resource):
    @api.expect(user_registration_model)
    @api.response(201, 'User created successfully', user_response_model)
    @api.response(400, 'Bad request - validation error')
    @api.response(409, 'User already exists')
    def post(self):
        """
        Register a new user with password hashing.

        This endpoint creates a new user account with a securely hashed password.
        The password is never stored in plain text and is not returned in responses.
        """
        try:
            # Get user data from request payload
            user_data = api.payload

            # Validate required fields
            if not user_data or 'email' not in user_data or 'password' not in user_data:
                return {
                    'error': 'Email and password are required'
                }, 400

            email = user_data['email']
            password = user_data['password']
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
            new_user = User.create_user(
                email=email,
                password=password,  # Will be hashed in __init__
                first_name=first_name,
                last_name=last_name,
                is_admin=is_admin
            )

            # Save to database
            db.session.add(new_user)
            db.session.commit()

            # Return user data (password excluded)
            return new_user.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            return {
                'error': f'User registration failed: {str(e)}'
            }, 500


@api.route('/<string:user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.response(200, 'User retrieved successfully', user_response_model)
    @api.response(404, 'User not found')
    @api.response(401, 'Unauthorized')
    def get(self, user_id):
        """
        Get user information by ID.

        This endpoint returns user data excluding the password hash for security.
        """
        try:
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
                'error': f'Failed to retrieve user: {str(e)}'
            }, 500


@api.route('/me')
class CurrentUser(Resource):
    @jwt_required()
    @api.response(200, 'Current user retrieved successfully', user_response_model)
    @api.response(404, 'User not found')
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
                'error': f'Failed to retrieve current user: {str(e)}'
            }, 500 