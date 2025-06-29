"""
JWT Authentication endpoints for the HBnB API.
Handles user login, token generation, and protected endpoints.
"""

import re
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    create_refresh_token, get_jwt
)
from werkzeug.security import check_password_hash
from datetime import timedelta

# Import the User model
from app.models.user import User

api = Namespace('auth', description='Authentication operations')

# Email validation regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(
        required=True, 
        description='User email address',
        example='user@example.com'
    ),
    'password': fields.String(
        required=True, 
        description='User password',
        example='securepassword123'
    )
})

# Model for response validation
token_response_model = api.model('TokenResponse', {
    'access_token': fields.String(description='JWT access token'),
    'refresh_token': fields.String(description='JWT refresh token'),
    'token_type': fields.String(description='Token type (Bearer)'),
    'expires_in': fields.Integer(
        description='Token expiration time in seconds'
    )
})

# Model for protected endpoint response
protected_response_model = api.model('ProtectedResponse', {
    'message': fields.String(description='Response message'),
    'user_id': fields.String(description='User ID from token'),
    'is_admin': fields.Boolean(description='User admin status')
})

# Model for error responses
error_model = api.model('Error', {
    'error': fields.String(description='Error message'),
    'details': fields.String(description='Additional error details', required=False)
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


def validate_credentials(email, password):
    """
    Validate login credentials format.
    
    Args:
        email (str): Email to validate
        password (str): Password to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not email or not password:
        return False, "Email and password are required"
    
    if not validate_email(email):
        return False, "Invalid email format"
    
    if not isinstance(password, str) or len(password) < 1:
        return False, "Password is required"
    
    return True, None


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login successful', token_response_model)
    @api.response(401, 'Invalid credentials', error_model)
    @api.response(400, 'Bad request', error_model)
    @api.response(500, 'Internal server error', error_model)
    def post(self):
        """
        Authenticate user and return JWT tokens.

        This endpoint validates user credentials and generates
        JWT access and refresh tokens upon successful authentication.
        """
        try:
            # Get credentials from request payload
            credentials = api.payload

            # Validate request body
            if not credentials:
                return {
                    'error': 'Request body is required'
                }, 400

            email = credentials.get('email')
            password = credentials.get('password')

            # Validate credentials format
            is_valid, error_message = validate_credentials(email, password)
            if not is_valid:
                return {
                    'error': error_message
                }, 400

            # Step 1: Retrieve the user based on the provided email
            user = User.get_by_email(email)

            # Step 2: Check if the user exists and the password is correct
            if not user or not user.verify_password(password):
                return {
                    'error': 'Invalid credentials'
                }, 401

            # Step 3: Create JWT tokens with user claims
            try:
                access_token = create_access_token(
                    identity=str(user.id),
                    additional_claims={
                        'is_admin': user.is_admin
                    },
                    expires_delta=timedelta(hours=1)
                )

                refresh_token = create_refresh_token(
                    identity=str(user.id),
                    additional_claims={
                        'is_admin': user.is_admin
                    },
                    expires_delta=timedelta(days=30)
                )
            except Exception as e:
                return {
                    'error': 'Token generation failed',
                    'details': str(e)
                }, 500

            # Step 4: Return JWT tokens to the client
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer',
                'expires_in': 3600  # 1 hour in seconds
            }, 200

        except Exception as e:
            return {
                'error': 'Authentication failed',
                'details': str(e)
            }, 500


@api.route('/refresh')
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    @api.response(200, 'Token refreshed', token_response_model)
    @api.response(401, 'Invalid refresh token', error_model)
    @api.response(500, 'Internal server error', error_model)
    def post(self):
        """
        Refresh JWT access token using refresh token.

        This endpoint allows clients to get a new access token
        using their refresh token without re-authenticating.
        """
        try:
            # Get current user identity from refresh token
            current_user_id = get_jwt_identity()
            current_claims = get_jwt()

            # Validate user still exists
            user = User.get_by_id(current_user_id)
            if not user:
                return {
                    'error': 'User not found'
                }, 401

            # Create new access token
            try:
                access_token = create_access_token(
                    identity=current_user_id,
                    additional_claims={
                        'is_admin': current_claims.get('is_admin', False)
                    },
                    expires_delta=timedelta(hours=1)
                )
            except Exception as e:
                return {
                    'error': 'Token generation failed',
                    'details': str(e)
                }, 500

            return {
                'access_token': access_token,
                'token_type': 'Bearer',
                'expires_in': 3600
            }, 200

        except Exception as e:
            return {
                'error': 'Token refresh failed',
                'details': str(e)
            }, 500


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    @api.response(200, 'Access granted', protected_response_model)
    @api.response(401, 'Invalid or missing token', error_model)
    @api.response(500, 'Internal server error', error_model)
    def get(self):
        """
        A protected endpoint that requires a valid JWT token.

        This endpoint demonstrates how to protect resources
        and extract user information from JWT tokens.
        """
        try:
            # Get current user identity from token
            current_user_id = get_jwt_identity()
            current_claims = get_jwt()

            # Validate user still exists
            user = User.get_by_id(current_user_id)
            if not user:
                return {
                    'error': 'User not found'
                }, 401

            # Extract user information from token claims
            is_admin = current_claims.get('is_admin', False)

            return {
                'message': f'Hello, user {current_user_id}',
                'user_id': current_user_id,
                'is_admin': is_admin
            }, 200

        except Exception as e:
            return {
                'error': 'Protected resource access failed',
                'details': str(e)
            }, 500


@api.route('/logout')
class Logout(Resource):
    @jwt_required()
    @api.response(200, 'Logout successful')
    @api.response(401, 'Invalid token', error_model)
    @api.response(500, 'Internal server error', error_model)
    def post(self):
        """
        Logout endpoint (token invalidation).

        In a production environment, you would typically
        add the token to a blacklist or use token revocation.
        """
        try:
            # Get token information
            jti = get_jwt()['jti']  # JWT ID

            # In a real implementation, you would add this token to a blacklist
            # blacklist.add(jti)

            return {
                'message': 'Successfully logged out',
                'token_id': jti
            }, 200

        except Exception as e:
            return {
                'error': 'Logout failed',
                'details': str(e)
            }, 500
