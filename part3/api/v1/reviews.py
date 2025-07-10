"""
Reviews management endpoints for the HBnB API.
Handles CRUD operations for reviews with authenticated user access.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.user import User
from app.services.facade import Facade
facade = Facade()

# Create API namespace
api = Namespace('reviews', description='Reviews management operations')

# Input validation models
review_creation_model = api.model('ReviewCreation', {
    'place_id': fields.String(
        required=True,
        description='ID of the place being reviewed',
        example='123e4567-e89b-12d3-a456-426614174000'
    ),
    'rating': fields.Integer(
        required=True,
        description='Rating from 1 to 5',
        example=5
    ),
    'comment': fields.String(
        description='Review comment',
        example='Great place to stay!'
    )
})

review_update_model = api.model('ReviewUpdate', {
    'rating': fields.Integer(description='Rating from 1 to 5'),
    'comment': fields.String(description='Review comment')
})

# Response models
review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'place_id': fields.String(description='Place ID'),
    'user_id': fields.String(description='User ID who wrote the review'),
    'rating': fields.Integer(description='Rating from 1 to 5'),
    'comment': fields.String(description='Review comment'),
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
    """Mock Place class for demonstration."""

    def __init__(self, id, owner_id):
        self.id = id
        self.owner_id = owner_id


class Review:
    """
    Review model for demonstration purposes.
    In a real implementation, this would be a SQLAlchemy model.
    """

    def __init__(self, id, place_id, user_id, rating, comment):
        self.id = id
        self.place_id = place_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
        self.created_at = None
        self.updated_at = None

    def to_dict(self):
        """Convert review object to dictionary."""
        return {
            'id': self.id,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


# Mock databases for demonstration
places_db = {}
reviews_db = {}


def get_place_by_id(place_id):
    """Get place by ID from mock database."""
    return places_db.get(place_id)


def get_review_by_id(review_id):
    """Get review by ID from mock database."""
    return reviews_db.get(review_id)


def get_reviews_by_place(place_id):
    """Get all reviews for a specific place."""
    return [review for review in reviews_db.values()
            if review.place_id == place_id]


def get_user_review_for_place(user_id, place_id):
    """Get user's review for a specific place."""
    for review in reviews_db.values():
        if review.user_id == user_id and review.place_id == place_id:
            return review
    return None


def create_review(review_data, user_id):
    """Create a new review in mock database."""
    import uuid
    review_id = str(uuid.uuid4())
    review = Review(
        id=review_id,
        place_id=review_data.get('place_id'),
        user_id=user_id,
        rating=review_data.get('rating'),
        comment=review_data.get('comment')
    )
    reviews_db[review_id] = review
    return review


def update_review(review_id, review_data):
    """Update review in mock database."""
    review = reviews_db.get(review_id)
    if not review:
        return None

    for field, value in review_data.items():
        if hasattr(review, field) and value is not None:
            setattr(review, field, value)

    return review


def delete_review(review_id):
    """Delete review from mock database."""
    if review_id in reviews_db:
        del reviews_db[review_id]
        return True
    return False


def get_all_reviews():
    """Get all reviews from mock database."""
    return list(reviews_db.values())


def validate_review_data(review_data):
    """
    Validate review data.

    Args:
        review_data (dict): Review data to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not review_data:
        return False, "Review data is required"

    # Validate place_id
    if not review_data.get('place_id'):
        return False, "Place ID is required"

    # Validate rating
    rating = review_data.get('rating')
    if rating is None:
        return False, "Rating is required"

    try:
        rating = int(rating)
        if not 1 <= rating <= 5:
            return False, "Rating must be between 1 and 5"
    except (ValueError, TypeError):
        return False, "Invalid rating value"

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
class ReviewsList(Resource):
    """Resource for listing and creating reviews."""

    @api.response(200, 'Reviews retrieved successfully')
    @api.response(500, 'Internal server error', error_model)
    def get(self):
        """
        Get all reviews (public endpoint).

        This endpoint returns all reviews and is accessible without
        authentication.
        """
        try:
            reviews = get_all_reviews()
            return {
                'reviews': [review.to_dict() for review in reviews],
                'total': len(reviews)
            }, 200
        except Exception as e:
            return {
                'error': 'Failed to retrieve reviews',
                'details': str(e)
            }, 500

    @jwt_required()
    @api.expect(review_creation_model)
    @api.response(201, 'Review created successfully', review_response_model)
    @api.response(400, 'Bad request', error_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Forbidden - cannot review own place', error_model)
    @api.response(409, 'Review already exists', error_model)
    @api.response(404, 'Place not found', error_model)
    @api.response(500, 'Internal server error', error_model)
    def post(self):
        """
        Create a new review (authenticated endpoint).

        This endpoint requires authentication and creates a new review.
        Users cannot review places they own or review the same place twice.
        """
        try:
            # Get current user
            user = get_current_user()
            if not user:
                return {
                    'error': 'User not found'
                }, 401

            # Get and validate review data
            review_data = api.payload
            is_valid, error_message = validate_review_data(review_data)

            if not is_valid:
                return {
                    'error': error_message
                }, 400

            place_id = api.payload.get('place_id')

            # Verifica que el lugar exista usando el Facade
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            # Check if user owns the place (cannot review own place)
            if place['owner_id'] == str(user.id):
                return {'error': 'You cannot review your own place'}, 403

            # Check if user already reviewed this place
            existing_review = get_user_review_for_place(str(user.id), place_id)
            if existing_review:
                return {
                    'error': 'You have already reviewed this place'
                }, 409

            # Create new review
            new_review = create_review(review_data, str(user.id))
            if not new_review:
                return {
                    'error': 'Failed to create review'
                }, 500

            return new_review.to_dict(), 201

        except Exception as e:
            return {
                'error': 'Failed to create review',
                'details': str(e)
            }, 500


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    """Resource for individual review operations."""

    @api.response(200, 'Review retrieved successfully', review_response_model)
    @api.response(400, 'Bad request', error_model)
    @api.response(404, 'Review not found', error_model)
    @api.response(500, 'Internal server error', error_model)
    def get(self, review_id):
        """
        Get review by ID (public endpoint).

        This endpoint returns a specific review and is accessible without
        authentication.
        """
        try:
            # Validate review_id
            if not review_id:
                return {
                    'error': 'Review ID is required'
                }, 400

            # Get review from database
            review = get_review_by_id(review_id)
            if not review:
                return {
                    'error': 'Review not found'
                }, 404

            return review.to_dict(), 200

        except Exception as e:
            return {
                'error': 'Failed to retrieve review',
                'details': str(e)
            }, 500

    @jwt_required()
    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully', review_response_model)
    @api.response(400, 'Bad request', error_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Forbidden - not the author', error_model)
    @api.response(404, 'Review not found', error_model)
    @api.response(500, 'Internal server error', error_model)
    def put(self, review_id):
        """
        Update review by ID (authenticated endpoint with ownership check).

        This endpoint requires authentication and ownership of the review.
        Users can only update reviews they wrote.
        """
        try:
            # Validate review_id
            if not review_id:
                return {
                    'error': 'Review ID is required'
                }, 400

            # Get current user
            user = get_current_user()
            if not user:
                return {
                    'error': 'User not found'
                }, 401

            # Get review from database
            review = get_review_by_id(review_id)
            if not review:
                return {
                    'error': 'Review not found'
                }, 404

            # Check ownership (admin bypass)
            current_claims = get_jwt()
            is_admin = current_claims.get('is_admin', False)

            if review.user_id != str(user.id) and not is_admin:
                return {
                    'error': 'Forbidden - you can only update your own reviews'
                }, 403

            # Get and validate update data
            update_data = api.payload
            if update_data:
                # Validate rating if provided
                if 'rating' in update_data:
                    try:
                        rating = int(update_data['rating'])
                        if not 1 <= rating <= 5:
                            return {
                                'error': 'Rating must be between 1 and 5'
                            }, 400
                    except (ValueError, TypeError):
                        return {
                            'error': 'Invalid rating value'
                        }, 400

            # Update review
            updated_review = update_review(review_id, update_data)
            if not updated_review:
                return {
                    'error': 'Failed to update review'
                }, 500

            return updated_review.to_dict(), 200

        except Exception as e:
            return {
                'error': 'Failed to update review',
                'details': str(e)
            }, 500

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(400, 'Bad request', error_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Forbidden - not the author', error_model)
    @api.response(404, 'Review not found', error_model)
    @api.response(500, 'Internal server error', error_model)
    def delete(self, review_id):
        """
        Delete review by ID (authenticated endpoint with ownership check).

        This endpoint requires authentication and ownership of the review.
        Users can only delete reviews they wrote.
        """
        try:
            # Validate review_id
            if not review_id:
                return {
                    'error': 'Review ID is required'
                }, 400

            # Get current user
            user = get_current_user()
            if not user:
                return {
                    'error': 'User not found'
                }, 401

            # Get review from database
            review = get_review_by_id(review_id)
            if not review:
                return {
                    'error': 'Review not found'
                }, 404

            # Check ownership (admin bypass)
            current_claims = get_jwt()
            is_admin = current_claims.get('is_admin', False)

            if review.user_id != str(user.id) and not is_admin:
                return {
                    'error': 'Forbidden - you can only delete your own reviews'
                }, 403

            # Delete review
            success = delete_review(review_id)
            if not success:
                return {
                    'error': 'Failed to delete review'
                }, 500

            return {
                'message': 'Review deleted successfully',
                'review_id': review_id
            }, 200

        except Exception as e:
            return {
                'error': 'Failed to delete review',
                'details': str(e)
            }, 500


@api.route('/place/<string:place_id>')
class PlaceReviews(Resource):
    """Resource for place-specific reviews."""

    @api.response(200, 'Place reviews retrieved successfully')
    @api.response(404, 'Place not found', error_model)
    @api.response(500, 'Internal server error', error_model)
    def get(self, place_id):
        """
        Get all reviews for a specific place (public endpoint).

        This endpoint returns all reviews for a specific place and is
        accessible without authentication.
        """
        try:
            # Validate place_id
            if not place_id:
                return {
                    'error': 'Place ID is required'
                }, 400

            # Check if place exists
            place = facade.get_place(place_id)
            if not place:
                return {
                    'error': 'Place not found'
                }, 404

            # Get reviews for the place
            reviews = get_reviews_by_place(place_id)
            return {
                'reviews': [review.to_dict() for review in reviews],
                'total': len(reviews),
                'place_id': place_id
            }, 200

        except Exception as e:
            return {
                'error': 'Failed to retrieve place reviews',
                'details': str(e)
            }, 500
