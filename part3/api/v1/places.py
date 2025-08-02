"""
Places management endpoints for the HBnB API.
Handles CRUD operations for places with authenticated user access.
"""

from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import jwt_required
from app.models.user import User
from api.v1.utils import get_current_user, is_admin_user, check_ownership_or_admin
from app.models.place import Place
from app import db
from datetime import datetime
from app.services.facade import Facade
facade = Facade()

api = Namespace('places', description='Places management operations')

place_model = api.model('Place', {
    'name': fields.String(required=True, description='Place name'),
    'description': fields.String(required=False, description='Place description'),
    'address': fields.String(required=False, description='Place address'),
    'price_per_night': fields.Float(required=False, description='Price per night'),
    'max_guests': fields.Integer(required=False, description='Maximum number of guests'),
    'latitude': fields.Float(required=False, description='Latitude coordinate'),
    'longitude': fields.Float(required=False, description='Longitude coordinate')
})

error_model = {
    'error': fields.String(description='Error message'),
    'details': fields.String(
        description='Additional error details',
        required=False
    )
}





# Using centralized function from utils.py


@api.route('/')
class PlacesList(Resource):
    def get(self):
        """
        Get all places (public endpoint).
        """
        try:
            places = facade.get_all_places()
            return {
                'places': places,
                'count': len(places)
            }, 200
        except Exception as e:
            return {
                'error': 'Failed to retrieve places',
                'details': str(e)
            }, 500

    @jwt_required()
    @api.expect(place_model)
    def post(self):
        """
        Create a new place (authenticated endpoint).
        """
        try:
            args = api.payload
            
            # Get current user
            user = get_current_user()
            if not user:
                return {'error': 'User not found'}, 401
            
            # Validate required fields
            if not args.get('name'):
                return {'error': 'Name is required'}, 400
            
            # Create place data with owner_id
            place_data = {
                'name': args['name'],
                'description': args.get('description'),
                'address': args.get('address'),
                'price_per_night': args.get('price_per_night'),
                'max_guests': args.get('max_guests'),
                'latitude': args.get('latitude'),
                'longitude': args.get('longitude'),
                'owner_id': user.id
            }
            
            # Create place using facade
            place = facade.create_place(place_data, user.id)
            if not place:
                return {'error': 'Failed to create place'}, 500
            
            return {
                'message': 'Place created successfully',
                'place': place
            }, 201
            
        except Exception as e:
            return {
                'error': 'Failed to create place',
                'details': str(e)
            }, 500


@api.route('/<string:place_id>')
class PlaceResource(Resource):
    """Resource for individual place operations."""

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

            return place, 200

        except Exception as e:
            return {
                'error': 'Failed to retrieve place',
                'details': str(e)
            }, 500

    @jwt_required()
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
            args = place_update_parser.parse_args()
            if args:
                is_valid, error_message = Facade.validate_place_update_data(args)
                if not is_valid:
                    return {
                        'error': error_message
                    }, 400

            # Update place
            updated_place = facade.update_place(place_id, args)
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
