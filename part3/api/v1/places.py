"""
Places management endpoints for the HBnB API.
Handles CRUD operations for places with authenticated user access.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.models.user import User
from api.v1.utils import get_current_user, is_admin_user, check_ownership_or_admin
from app.models.place import Place
from app import db
from datetime import datetime
from app.services.facade import Facade
facade = Facade()

# Create API namespace
api = Namespace('places', description='Places management operations')

# Input validation models
place_creation_model = api.model('PlaceCreation', {
    'name': fields.String(
        required=True,
        description='Place name',
        example='Cozy Apartment'
    ),
    'description': fields.String(
        description='Place description',
        example='A beautiful apartment in the city center'
    ),
    'address': fields.String(
        description='Place address',
        example='123 Main St, City, Country'
    ),
    'price_per_night': fields.Float(
        description='Price per night',
        example=100.50
    ),
    'max_guests': fields.Integer(
        description='Maximum number of guests',
        example=4
    ),
    'latitude': fields.Float(
        description='Latitude coordinate',
        example=40.7128
    ),
    'longitude': fields.Float(
        description='Longitude coordinate',
        example=-74.0060
    )
})

place_update_model = api.model('PlaceUpdate', {
    'name': fields.String(description='Place name'),
    'description': fields.String(description='Place description'),
    'address': fields.String(description='Place address'),
    'price_per_night': fields.Float(description='Price per night'),
    'max_guests': fields.Integer(description='Maximum number of guests'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate')
})

# Response models
place_response_model = api.model('PlaceResponse', {
    'id': fields.String(description='Place ID'),
    'name': fields.String(description='Place name'),
    'description': fields.String(description='Place description'),
    'address': fields.String(description='Place address'),
    'price_per_night': fields.Float(description='Price per night'),
    'max_guests': fields.Integer(description='Maximum number of guests'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate'),
    'owner_id': fields.String(description='Owner user ID'),
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





# Using centralized function from utils.py


@api.route('/')
class PlacesList(Resource):
    """Resource for listing and creating places."""

    @api.response(200, 'Places retrieved successfully')
    @api.response(500, 'Internal server error', error_model)
    def get(self):
        """
        Get all places (public endpoint).

        This endpoint returns all places and is accessible without
        authentication.
        """
        try:
            places = facade.get_all_places()
            return {
                'places': [place for place in places],
                'total': len(places)
            }, 200
        except Exception as e:
            return {
                'error': 'Failed to retrieve places',
                'details': str(e)
            }, 500

    @jwt_required()
    @api.expect(place_creation_model)
    @api.response(201, 'Place created successfully', place_response_model)
    @api.response(400, 'Bad request', error_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(500, 'Internal server error', error_model)
    def post(self):
        """
        Create a new place (authenticated endpoint).

        This endpoint requires authentication and creates a new place
        owned by the authenticated user.
        """
        try:
            # Get current user
            user = get_current_user()
            if not user:
                return {
                    'error': 'User not found'
                }, 401

            # Get and validate place data
            place_data = api.payload
            is_valid, error_message = Facade.validate_place_data(place_data)

            if not is_valid:
                return {
                    'error': error_message
                }, 400

            # Create new place usando facade
            new_place = facade.create_place(place_data, str(user.id))
            if not new_place:
                return {
                    'error': 'Failed to create place'
                }, 500

            return new_place, 201

        except Exception as e:
            return {
                'error': 'Failed to create place',
                'details': str(e)
            }, 500


@api.route('/<string:place_id>')
class PlaceResource(Resource):
    """Resource for individual place operations."""

    @api.response(200, 'Place retrieved successfully', place_response_model)
    @api.response(400, 'Bad request', error_model)
    @api.response(404, 'Place not found', error_model)
    @api.response(500, 'Internal server error', error_model)
    def get(self, place_id):
        """
        Get place by ID (public endpoint).

        This endpoint returns a specific place and is accessible without
        authentication.
        """
        try:
            # Validate place_id
            if not place_id:
                return {
                    'error': 'Place ID is required'
                }, 400

            # Get place from database
            place = facade.get_place(place_id)
            if not place:
                return {
                    'error': 'Place not found'
                }, 404

            return place.to_dict(), 200

        except Exception as e:
            return {
                'error': 'Failed to retrieve place',
                'details': str(e)
            }, 500

    @jwt_required()
    @api.expect(place_update_model)
    @api.response(200, 'Place updated successfully', place_response_model)
    @api.response(400, 'Bad request', error_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Forbidden - not the owner', error_model)
    @api.response(404, 'Place not found', error_model)
    @api.response(500, 'Internal server error', error_model)
    def put(self, place_id):
        """
        Update a place (only owner can update).
        """
        try:
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            # Get current user
            user = get_current_user()
            if not user:
                return {
                    'error': 'User not found'
                }, 401

            # Check ownership (admin bypass)
            if not check_ownership_or_admin(place['owner_id'], user.id):
                return {
                    'error': 'Unauthorized - you do not own this place'
                }, 401

            # Get and validate update data
            update_data = api.payload
            if update_data:
                is_valid, error_message = Facade.validate_place_update_data(update_data)
                if not is_valid:
                    return {
                        'error': error_message
                    }, 400

            # Update place
            updated_place = facade.update_place(place_id, update_data)
            if not updated_place:
                return {
                    'error': 'Failed to update place'
                }, 500
            return updated_place, 200

        except Exception as e:
            return {
                'error': 'Failed to update place',
                'details': str(e)
            }, 500

    @jwt_required()
    @api.response(200, 'Place deleted successfully')
    @api.response(400, 'Bad request', error_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Forbidden - not the owner', error_model)
    @api.response(404, 'Place not found', error_model)
    @api.response(500, 'Internal server error', error_model)
    def delete(self, place_id):
        """
        Delete place by ID (authenticated endpoint with ownership check).

        This endpoint requires authentication and ownership of the place.
        Users can only delete places they own.
        """
        try:
            # Validate place_id
            if not place_id:
                return {
                    'error': 'Place ID is required'
                }, 400

            # Get current user
            user = get_current_user()
            if not user:
                return {
                    'error': 'User not found'
                }, 401

            # Get place from database
            place = facade.get_place(place_id)
            if not place:
                return {
                    'error': 'Place not found'
                }, 404

            # Check ownership (admin bypass)
            if not check_ownership_or_admin(place['owner_id'], user.id):
                return {
                    'error': 'Unauthorized - you do not own this place'
                }, 401

            # Delete place
            success = facade.delete_place(place_id)
            if not success:
                return {
                    'error': 'Failed to delete place'
                }, 500

            return {
                'message': 'Place deleted successfully',
                'place_id': place_id
            }, 200

        except Exception as e:
            return {
                'error': 'Failed to delete place',
                'details': str(e)
            }, 500
