"""
Reviews management endpoints for the HBnB API.
Handles CRUD operations for reviews with authenticated user access.
"""

from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.user import User
from app.services.facade import Facade
facade = Facade()

api = Namespace('reviews', description='Reviews management operations')

review_model = api.model('Review', {
    'place_id': fields.String(required=True, description='ID of the place being reviewed'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5'),
    'comment': fields.String(required=False, description='Review comment')
})

review_update_parser = reqparse.RequestParser()
review_update_parser.add_argument('rating', type=int, required=False)
review_update_parser.add_argument('comment', type=str, required=False)

error_model = {
    'error': fields.String(description='Error message'),
    'details': fields.String(
        description='Additional error details',
        required=False
    )
}


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
    try:
        current_user_id = get_jwt_identity()
        print(f"[DEBUG] current_user_id from JWT: {current_user_id}")
        if not current_user_id:
            return None
        user = User.get_by_id(current_user_id)
        print(f"[DEBUG] User.get_by_id({current_user_id}) result: {user}")
        return user
    except Exception as e:
        print(f"Error getting current user: {e}")
        return None


@api.route('/')
class ReviewsList(Resource):
    """Resource for listing and creating reviews."""

    @api.expect(review_model)
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
            args = api.payload
            is_valid, error_message = validate_review_data(args)

            if not is_valid:
                return {
                    'error': error_message
                }, 400

            place_id = args.get('place_id')

            # Check if the place exists using the Facade
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            # Check if user owns the place (cannot review own place)
            if place['owner_id'] == str(user.id):
                return {'error': 'You cannot review your own place'}, 403

            # Check if user already reviewed this place
            existing_review = facade.get_user_review_for_place(str(user.id), place_id)
            if existing_review:
                return {
                    'error': 'You have already reviewed this place'
                }, 409

            # Create new review
            new_review = facade.create_review(args, str(user.id))
            if not new_review:
                return {
                    'error': 'Failed to create review'
                }, 500

            return new_review, 201

        except Exception as e:
            return {
                'error': 'Failed to create review',
                'details': str(e)
            }, 500


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    """Resource for individual review operations."""

    # Eliminar: @api.response(200, 'Review retrieved successfully', review_response_model)
    # Eliminar: @api.response(400, 'Bad request', error_model)
    # Eliminar: @api.response(404, 'Review not found', error_model)
    # Eliminar: @api.response(500, 'Internal server error', error_model)
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
            review = facade.get_review(review_id)
            if not review:
                return {
                    'error': 'Review not found'
                }, 404

            return review, 200

        except Exception as e:
            return {
                'error': 'Failed to retrieve review',
                'details': str(e)
            }, 500

    @jwt_required()
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
            review = facade.get_review(review_id)
            if not review:
                return {
                    'error': 'Review not found'
                }, 404

            # Check ownership (admin bypass)
            current_claims = get_jwt()
            is_admin = current_claims.get('is_admin', False)

            if review['user_id'] != str(user.id) and not is_admin:
                return {
                    'error': 'Forbidden - you can only update your own reviews'
                }, 403

            # Get and validate update data
            args = review_update_parser.parse_args()
            if args:
                # Validate rating if provided
                if 'rating' in args:
                    try:
                        rating = int(args['rating'])
                        if not 1 <= rating <= 5:
                            return {
                                'error': 'Rating must be between 1 and 5'
                            }, 400
                    except (ValueError, TypeError):
                        return {
                            'error': 'Invalid rating value'
                        }, 400

            # Update review
            updated_review = facade.update_review(review_id, args)
            if not updated_review:
                return {
                    'error': 'Failed to update review'
                }, 500

            return updated_review, 200

        except Exception as e:
            return {
                'error': 'Failed to update review',
                'details': str(e)
            }, 500

    @jwt_required()
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
            review = facade.get_review(review_id)
            if not review:
                return {
                    'error': 'Review not found'
                }, 404

            # Check ownership (admin bypass)
            current_claims = get_jwt()
            is_admin = current_claims.get('is_admin', False)

            if review['user_id'] != str(user.id) and not is_admin:
                return {
                    'error': 'Forbidden - you can only delete your own reviews'
                }, 403

            # Delete review
            success = facade.delete_review(review_id)
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

    # Eliminar: @api.response(200, 'Place reviews retrieved successfully')
    # Eliminar: @api.response(404, 'Place not found', error_model)
    # Eliminar: @api.response(500, 'Internal server error', error_model)
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
            reviews = facade.get_reviews_by_place(place_id)
            return {
                'reviews': reviews,
                'total': len(reviews),
                'place_id': place_id
            }, 200

        except Exception as e:
            return {
                'error': 'Failed to retrieve place reviews',
                'details': str(e)
            }, 500
