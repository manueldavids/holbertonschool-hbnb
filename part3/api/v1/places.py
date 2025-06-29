"""
Places management endpoints for the HBnB API.
Handles CRUD operations for places with authenticated user access.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User

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


def validate_place_data(place_data):
    """
    Validate place data.

    Args:
        place_data (dict): Place data to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not place_data or 'name' not in place_data:
        return False, "Place name is required"

    # Validate price_per_night
    if 'price_per_night' in place_data:
        try:
            price = float(place_data['price_per_night'])
            if price < 0:
                return False, "Price per night cannot be negative"
        except (ValueError, TypeError):
            return False, "Invalid price per night value"

    # Validate max_guests
    if 'max_guests' in place_data:
        try:
            guests = int(place_data['max_guests'])
            if guests <= 0:
                return False, "Maximum guests must be positive"
        except (ValueError, TypeError):
            return False, "Invalid maximum guests value"

    # Validate coordinates
    if 'latitude' in place_data:
        try:
            lat = float(place_data['latitude'])
            if not -90 <= lat <= 90:
                return False, "Latitude must be between -90 and 90"
        except (ValueError, TypeError):
            return False, "Invalid latitude value"

    if 'longitude' in place_data:
        try:
            lon = float(place_data['longitude'])
            if not -180 <= lon <= 180:
                return False, "Longitude must be between -180 and 180"
        except (ValueError, TypeError):
            return False, "Invalid longitude value"

    return True, ""


def get_current_user():
    """
    Get current authenticated user.

    Returns:
        User: Current user instance or None
    """
    try:
        current_user_id = get_jwt_identity()
        return User.get_by_id(current_user_id)
    except Exception:
        return None


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
            # Get current user
            user = get_current_user()
            if not user:
                return {
                    'error': 'User not found'
                }, 401

            # Get and validate place data
            place_data = api.payload
            is_valid, error_message = validate_place_data(place_data)

            if not is_valid:
                return {
                    'error': error_message
                }, 400

            # Create new place
            new_place = create_place(place_data, str(user.id))
            if not new_place:
                return {
                    'error': 'Failed to create place'
                }, 500

            return new_place.to_dict(), 201

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
            place = get_place_by_id(place_id)
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

            # Get current user
            user = get_current_user()
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
            if place.owner_id != str(user.id):
                return {
                    'error': 'Forbidden - you can only update your own places'
                }, 403

            # Get and validate update data
            update_data = api.payload
            if update_data:
                is_valid, error_message = validate_place_data(update_data)
                if not is_valid:
                    return {
                        'error': error_message
                    }, 400

            # Update place
            updated_place = update_place(place_id, update_data)
            if not updated_place:
                return {
                    'error': 'Failed to update place'
                }, 500

            return updated_place.to_dict(), 200

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
            place = get_place_by_id(place_id)
            if not place:
                return {
                    'error': 'Place not found'
                }, 404

            # Check ownership
            if place.owner_id != str(user.id):
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
