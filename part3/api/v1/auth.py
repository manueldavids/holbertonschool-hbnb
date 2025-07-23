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
from .response_utils import APIResponse, handle_exceptions
from .validation_utils import ValidationUtils
from app.services.facade import Facade
facade = Facade()

api = Namespace('auth', description='Authentication operations')

# Define models and parsers as needed
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password')
})


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

    is_valid, error = ValidationUtils.validate_email(email)
    if not is_valid:
        return False, "Invalid email format"

    if not isinstance(password, str) or len(password) < 1:
        return False, "Password is required"

    return True, None


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """
        Authenticate user and return JWT tokens.
        """
        args = api.payload
        email = args['email']
        password = args['password']
        # Validación y autenticación igual que antes
        is_valid, error_message = validate_credentials(email, password)
        if not is_valid:
            return {'error': error_message}, 400
        user = facade.authenticate_user(email, password)
        if not user:
            return {'error': 'Invalid credentials'}, 401
        try:
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={'is_admin': user.is_admin},
                expires_delta=timedelta(hours=1)
            )
            refresh_token = create_refresh_token(
                identity=str(user.id),
                additional_claims={'is_admin': user.is_admin},
                expires_delta=timedelta(days=30)
            )
        except Exception as e:
            return {'error': 'Token generation failed', 'details': str(e)}, 500
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': 3600,
            'message': 'Login successful'
        }, 200


@api.route('/refresh')
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
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
                return {'error': 'User not found'}, 401

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
                return {'error': 'Token generation failed', 'details': str(e)}, 500

            return {
                'access_token': access_token,
                'token_type': 'Bearer',
                'expires_in': 3600,
                'message': 'Token refreshed successfully'
            }, 200

        except Exception as e:
            return {'error': 'Token refresh failed', 'details': str(e)}, 500


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
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
                return {'error': 'User not found'}, 401

            # Extract user information from token claims
            is_admin = current_claims.get('is_admin', False)

            return {
                'message': f'Hello, user {current_user_id}',
                'user_id': current_user_id,
                'is_admin': is_admin
            }, 200

        except Exception as e:
            return {'error': 'Protected resource access failed', 'details': str(e)}, 500


@api.route('/logout')
class Logout(Resource):
    @jwt_required()
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
            return {'error': 'Logout failed', 'details': str(e)}, 500
