"""
Administrator access endpoints for the HBnB API.
Handles admin-only operations with role-based access control.
"""
import re
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from app.models.user import User, db
from app.models.amenity import Amenity
from api.v1.utils import (
    get_current_admin_user, 
    validate_email, 
    validate_password,
    handle_database_error
)
# Create API namespace
api = Namespace('admin', description='Administrator operations')
# Email validation regex (keeping for backward compatibility)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
# Input validation models
admin_user_creation_model = api.model('AdminUserCreation', {
    'email': fields.String(
        required=True,
        description='User email address',
        example='newuser@example.com'
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
admin_user_update_model = api.model('AdminUserUpdate', {
    'email': fields.String(description='User email address'),
    'password': fields.String(description='User password'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'is_admin': fields.Boolean(description='Admin privileges flag')
})
amenity_creation_model = api.model('AmenityCreation', {
    'name': fields.String(
        required=True,
        description='Amenity name',
        example='WiFi'
    ),
    'description': fields.String(
        description='Amenity description',
        example='High-speed wireless internet'
    )
})
amenity_update_model = api.model('AmenityUpdate', {
    'name': fields.String(description='Amenity name'),
    'description': fields.String(description='Amenity description')
})
# Response models
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'email': fields.String(description='User email address'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'is_admin': fields.Boolean(description='Admin privileges flag'),
    'created_at': fields.String(description='User creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})
amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name'),
    'description': fields.String(description='Amenity description'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})
error_model = api.model('Error', {
    'error': fields.String(description='Error message'),
    'details': fields.String(
        description='Additional error details',
        required=False
    )
})


def get_amenity_by_id(amenity_id):
    """Get amenity by ID from database."""
    return Amenity.get_by_id(amenity_id)


def create_amenity(amenity_data):
    """Create a new amenity in database."""
    return Amenity.create(
        name=amenity_data.get('name'),
        description=amenity_data.get('description')
    )


def update_amenity(amenity_id, amenity_data):
    """Update amenity in database."""
    amenity = Amenity.get_by_id(amenity_id)
    if not amenity:
        return None
    if amenity.update_from_dict(amenity_data):
        db.session.commit()
        return amenity
    return None


def delete_amenity(amenity_id):
    """Delete amenity from database."""
    amenity = Amenity.get_by_id(amenity_id)
    if not amenity:
        return False
    return amenity.delete()


def get_all_amenities():
    """Get all amenities from database."""
    return Amenity.get_all()


# Using centralized validation functions from utils.py


# Using centralized function from utils.py


@api.route('/users')
class AdminUserManagement(Resource):
    """Resource for admin user management operations."""
    @jwt_required()
    @api.expect(admin_user_creation_model)
    @api.response(201, 'User created successfully', user_response_model)
    @api.response(400, 'Bad request', error_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Forbidden - admin access required', error_model)
    @api.response(409, 'User already exists', error_model)
    @api.response(500, 'Internal server error', error_model)
    def post(self):
        """
        Create a new user (admin only).
        This endpoint allows administrators to create new user accounts.
        Only users with admin privileges can access this endpoint.
        """
        try:
            # Verify admin privileges
            admin_user = get_current_admin_user()
            if not admin_user:
                return {
                    'error': 'Forbidden - admin access required'
                }, 403
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
                'error': 'User creation failed',
                'details': str(e)
            }, 500

    @jwt_required()
    @api.response(200, 'Users retrieved successfully')
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Forbidden - admin access required', error_model)
    @api.response(500, 'Internal server error', error_model)
    def get(self):
        """
        Get all users (admin only).
        This endpoint returns a list of all users, excluding password hashes.
        Only admin users can access this endpoint.
        """
        try:
            # Verify admin privileges
            admin_user = get_current_admin_user()
            if not admin_user:
                return {
                    'error': 'Forbidden - admin access required'
                }, 403
            # Get all users
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


@api.route('/users/<string:user_id>')
class AdminUserResource(Resource):
    """Resource for individual admin user operations."""
    @jwt_required()
    @api.expect(admin_user_update_model)
    @api.response(200, 'User updated successfully', user_response_model)
    @api.response(400, 'Bad request', error_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Forbidden - admin access required', error_model)
    @api.response(404, 'User not found', error_model)
    @api.response(409, 'Email already exists', error_model)
    @api.response(500, 'Internal server error', error_model)
    def put(self, user_id):
        """
        Update any user's details (admin only).
        This endpoint allows administrators to update any user's data,
        including email and password. Only users with admin privileges
        can access this endpoint.
        """
        try:
            # Verify admin privileges
            admin_user = get_current_admin_user()
            if not admin_user:
                return {
                    'error': 'Forbidden - admin access required'
                }, 403
            # Validate user_id
            if not user_id:
                return {
                    'error': 'User ID is required'
                }, 400
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
            # Handle email update with validation
            if 'email' in update_data and update_data['email']:
                new_email = update_data['email']
                # Validate email format
                if not validate_email(new_email):
                    return {
                        'error': 'Invalid email format'
                    }, 400
                # Check if email is already taken by another user
                existing_user = User.get_by_email(new_email)
                if existing_user and str(existing_user.id) != user_id:
                    return {
                        'error': 'Email already exists'
                    }, 409
            # Handle password update with validation
            if 'password' in update_data and update_data['password']:
                password = update_data['password']
                is_valid_password, password_error = validate_password(password)
                if not is_valid_password:
                    return {
                        'error': password_error
                    }, 400
                # Hash the new password
                user.set_password(update_data['password'])
            # Update other user fields
            for field, value in update_data.items():
                if (hasattr(user, field) and value is not None and
                        field != 'password'):
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


@api.route('/amenities')
class AdminAmenityManagement(Resource):
    """Resource for admin amenity management operations."""
    @jwt_required()
    @api.expect(amenity_creation_model)
    @api.response(201, 'Amenity created successfully', amenity_response_model)
    @api.response(400, 'Bad request', error_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Forbidden - admin access required', error_model)
    @api.response(500, 'Internal server error', error_model)
    def post(self):
        """
        Create a new amenity (admin only).
        This endpoint allows administrators to create new amenities.
        Only users with admin privileges can access this endpoint.
        """
        try:
            # Verify admin privileges
            admin_user = get_current_admin_user()
            if not admin_user:
                return {
                    'error': 'Forbidden - admin access required'
                }, 403
            # Get amenity data from request payload
            amenity_data = api.payload
            # Validate required fields
            if not amenity_data or 'name' not in amenity_data:
                return {
                    'error': 'Amenity name is required'
                }, 400
            # Create new amenity
            new_amenity = create_amenity(amenity_data)
            if not new_amenity:
                return {
                    'error': 'Failed to create amenity'
                }, 500
            return new_amenity.to_dict(), 201
        except Exception as e:
            return {
                'error': 'Failed to create amenity',
                'details': str(e)
            }, 500

    @jwt_required()
    @api.response(200, 'Amenities retrieved successfully')
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Forbidden - admin access required', error_model)
    @api.response(500, 'Internal server error', error_model)
    def get(self):
        """
        Get all amenities (admin only).
        This endpoint returns a list of all amenities.
        Only admin users can access this endpoint.
        """
        try:
            # Verify admin privileges
            admin_user = get_current_admin_user()
            if not admin_user:
                return {
                    'error': 'Forbidden - admin access required'
                }, 403
            # Get all amenities
            amenities = get_all_amenities()
            return {
                'amenities': [amenity.to_dict() for amenity in amenities],
                'total': len(amenities)
            }, 200
        except Exception as e:
            return {
                'error': 'Failed to retrieve amenities',
                'details': str(e)
            }, 500


@api.route('/amenities/<string:amenity_id>')
class AdminAmenityResource(Resource):
    """Resource for individual admin amenity operations."""
    @jwt_required()
    @api.expect(amenity_update_model)
    @api.response(200, 'Amenity updated successfully', amenity_response_model)
    @api.response(400, 'Bad request', error_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Forbidden - admin access required', error_model)
    @api.response(404, 'Amenity not found', error_model)
    @api.response(500, 'Internal server error', error_model)
    def put(self, amenity_id):
        """
        Update amenity (admin only).
        This endpoint allows administrators to update amenities.
        Only users with admin privileges can access this endpoint.
        """
        try:
            # Verify admin privileges
            admin_user = get_current_admin_user()
            if not admin_user:
                return {
                    'error': 'Forbidden - admin access required'
                }, 403
            # Validate amenity_id
            if not amenity_id:
                return {
                    'error': 'Amenity ID is required'
                }, 400
            # Get amenity from database
            amenity = get_amenity_by_id(amenity_id)
            if not amenity:
                return {
                    'error': 'Amenity not found'
                }, 404
            # Get update data from request payload
            update_data = api.payload
            if not update_data:
                return {
                    'error': 'Update data is required'
                }, 400
            # Update amenity
            updated_amenity = update_amenity(amenity_id, update_data)
            if not updated_amenity:
                return {
                    'error': 'Failed to update amenity'
                }, 500
            return updated_amenity.to_dict(), 200
        except Exception as e:
            return {
                'error': 'Failed to update amenity',
                'details': str(e)
            }, 500

    @jwt_required()
    @api.response(200, 'Amenity deleted successfully')
    @api.response(400, 'Bad request', error_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Forbidden - admin access required', error_model)
    @api.response(404, 'Amenity not found', error_model)
    @api.response(500, 'Internal server error', error_model)
    def delete(self, amenity_id):
        """
        Delete amenity (admin only).
        This endpoint allows administrators to delete amenities.
        Only users with admin privileges can access this endpoint.
        """
        try:
            # Verify admin privileges
            admin_user = get_current_admin_user()
            if not admin_user:
                return {
                    'error': 'Forbidden - admin access required'
                }, 403
            # Validate amenity_id
            if not amenity_id:
                return {
                    'error': 'Amenity ID is required'
                }, 400
            # Get amenity from database
            amenity = get_amenity_by_id(amenity_id)
            if not amenity:
                return {
                    'error': 'Amenity not found'
                }, 404
            # Delete amenity
            success = delete_amenity(amenity_id)
            if not success:
                return {
                    'error': 'Failed to delete amenity'
                }, 500
            return {
                'message': 'Amenity deleted successfully',
                'amenity_id': amenity_id
            }, 200
        except Exception as e:
            return {
                'error': 'Failed to delete amenity',
                'details': str(e)
            }, 500
