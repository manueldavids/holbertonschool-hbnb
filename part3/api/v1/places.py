"""
Places management endpoints for the HBnB API.
Handles CRUD operations for places with authenticated user access.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy.exc import IntegrityError
from app.models.user import User, db

api = Namespace('places', description='Places management operations')

# Model for place creation input validation
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

# Model for place update input validation
place_update_model = api.model('PlaceUpdate', {
    'name': fields.String(description='Place name'),
    'description': fields.String(description='Place description'),
    'address': fields.String(description='Place address'),
    'price_per_night': fields.Float(description='Price per night'),
    'max_guests': fields.Integer(description='Maximum number of guests'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate')
})

# Model for place response
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

# Model for error responses
error_model = api.model('Error', {
    'error': fields.String(description='Error message'),
    'details': fields.String(
        description='Additional error details',
        required=False
    )
})


class Place:
    """
    Place model for demonstration purposes.
    In a real implementation, this would be a SQLAlchemy model.
    """

    def __init__(self, id, name, description, address, price_per_night,
                 max_guests, latitude, longitude, owner_id):
        self.id = id
        self.name = name
        self.description = description
        self.address = address
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.created_at = None
        self.updated_at = None

    def to_dict(self):
        """Convert place object to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


# Mock database for demonstration
places_db = {}


def get_place_by_id(place_id):
    """Get place by ID from mock database."""
    return places_db.get(place_id)


def create_place(place_data, owner_id):
    """Create a new place in mock database."""
    import uuid
    place_id = str(uuid.uuid4())
    place = Place(
        id=place_id,
        name=place_data.get('name'),
        description=place_data.get('description'),
        address=place_data.get('address'),
        price_per_night=place_data.get('price_per_night'),
        max_guests=place_data.get('max_guests'),
        latitude=place_data.get('latitude'),
        longitude=place_data.get('longitude'),
        owner_id=owner_id
    )
    places_db[place_id] = place
    return place


def update_place(place_id, place_data):
    """Update place in mock database."""
    place = places_db.get(place_id)
    if not place:
        return None

    for field, value in place_data.items():
        if hasattr(place, field) and value is not None:
            setattr(place, field, value)

    return place


def delete_place(place_id):
    """Delete place from mock database."""
    if place_id in places_db:
        del places_db[place_id]
        return True
    return False


def get_all_places():
    """Get all places from mock database."""
    return list(places_db.values())


@api.route('/')
class PlacesList(Resource):
    @api.response(200, 'Places retrieved successfully')
    @api.response(500, 'Internal server error', error_model)
    def get(self):
        """
        Get all places (public endpoint).

        This endpoint returns all places and is accessible without
        authentication.
        """
        try:
            places = get_all_places()
            return {
                'places': [place.to_dict() for place in places],
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
            # Get current user identity
            current_user_id = get_jwt_identity()

            # Verify user exists
            user = User.get_by_id(current_user_id)
            if not user:
                return {
                    'error': 'User not found'
                }, 401

            # Get place data from request payload
            place_data = api.payload

            # Validate required fields
            if not place_data or 'name' not in place_data:
                return {
                    'error': 'Place name is required'
                }, 400

            # Create new place
            new_place = create_place(place_data, current_user_id)

            # Return created place
            return new_place.to_dict(), 201

        except Exception as e:
            return {
                'error': 'Failed to create place',
                'details': str(e)
            }, 500


@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place retrieved successfully', place_response_model)
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
            place = get_place_by_id(place_id)
            if not place:
                return {
                    'error': 'Place not found'
                }, 404

            # Return place data
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
        Update place by ID (authenticated endpoint with ownership check).

        This endpoint requires authentication and ownership of the place.
        Users can only update places they own.
        """
        try:
            # Validate place_id
            if not place_id:
                return {
                    'error': 'Place ID is required'
                }, 400

            # Get current user identity
            current_user_id = get_jwt_identity()

            # Verify user exists
            user = User.get_by_id(current_user_id)
            if not user:
                return {
                    'error': 'User not found'
                }, 401

            # Get place from database
            place = get_place_by_id(place_id)
            if not place:
                return {
                    'error': 'Place not found'
                }, 404

            # Check ownership
            if place.owner_id != current_user_id:
                return {
                    'error': 'Forbidden - you can only update your own places'
                }, 403

            # Get update data from request payload
            update_data = api.payload

            # Update place
            updated_place = update_place(place_id, update_data)

            # Return updated place
            return updated_place.to_dict(), 200

        except Exception as e:
            return {
                'error': 'Failed to update place',
                'details': str(e)
            }, 500

    @jwt_required()
    @api.response(200, 'Place deleted successfully')
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

            # Get current user identity
            current_user_id = get_jwt_identity()

            # Verify user exists
            user = User.get_by_id(current_user_id)
            if not user:
                return {
                    'error': 'User not found'
                }, 401

            # Get place from database
            place = get_place_by_id(place_id)
            if not place:
                return {
                    'error': 'Place not found'
                }, 404

            # Check ownership
            if place.owner_id != current_user_id:
                return {
                    'error': 'Forbidden - you can only delete your own places'
                }, 403

            # Delete place
            success = delete_place(place_id)
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
