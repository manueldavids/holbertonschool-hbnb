from flask import request
from flask_restx import Namespace, Resource
from app.services import hbnb_facade
from app.api.v1.models import create_api_models

# Create namespace
api = Namespace('reviews', description='Review operations')

# Get API models
models = create_api_models(api)

@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    @api.marshal_list_with(models['review'])
    def get(self):
        """List all reviews"""
        try:
            reviews = hbnb_facade.get_all_reviews()
            return [review.to_dict() for review in reviews], 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('create_review')
    @api.expect(models['review'])
    @api.marshal_with(models['review'], code=201)
    def post(self):
        """Create a new review"""
        try:
            data = request.get_json()
            if not data:
                api.abort(400, "No data provided")
            
            review = hbnb_facade.create_review(data)
            if review:
                return review.to_dict(), 201
            else:
                api.abort(400, "Failed to create review")
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @api.doc('get_review')
    @api.marshal_with(models['review'])
    def get(self, review_id):
        """Get a review by ID"""
        try:
            review = hbnb_facade.get_review(review_id)
            if review:
                return review.to_dict(), 200
            else:
                api.abort(404, "Review not found")
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('update_review')
    @api.expect(models['review_update'])
    @api.marshal_with(models['review'])
    def put(self, review_id):
        """Update a review"""
        try:
            data = request.get_json()
            if not data:
                api.abort(400, "No data provided")
            
            success = hbnb_facade.update_review(review_id, data)
            if success:
                review = hbnb_facade.get_review(review_id)
                return review.to_dict(), 200
            else:
                api.abort(404, "Review not found")
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('delete_review')
    @api.response(204, 'Review deleted')
    def delete(self, review_id):
        """Delete a review"""
        try:
            success = hbnb_facade.delete_review(review_id)
            if success:
                return '', 204
            else:
                api.abort(404, "Review not found")
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

@api.route('/place/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceReviews(Resource):
    @api.doc('get_place_reviews')
    @api.marshal_list_with(models['review'])
    def get(self, place_id):
        """Get all reviews for a place"""
        try:
            reviews = hbnb_facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews], 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

@api.route('/user/<string:user_id>')
@api.param('user_id', 'The user identifier')
class UserReviews(Resource):
    @api.doc('get_user_reviews')
    @api.marshal_list_with(models['review'])
    def get(self, user_id):
        """Get all reviews by a user"""
        try:
            reviews = hbnb_facade.get_reviews_by_user(user_id)
            return [review.to_dict() for review in reviews], 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")