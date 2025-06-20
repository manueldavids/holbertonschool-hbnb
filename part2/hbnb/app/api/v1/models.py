from flask_restx import fields

# Create API models for request/response schemas
def create_api_models(api):
    # User models
    user_model = api.model('User', {
        'id': fields.String(readonly=True, description='User unique identifier'),
        'email': fields.String(required=True, description='User email address'),
        'password': fields.String(required=True, description='User password'),
        'first_name': fields.String(description='User first name'),
        'last_name': fields.String(description='User last name'),
        'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
        'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
    })

    user_response_model = api.model('UserResponse', {
        'id': fields.String(readonly=True, description='User unique identifier'),
        'email': fields.String(readonly=True, description='User email address'),
        'first_name': fields.String(readonly=True, description='User first name'),
        'last_name': fields.String(readonly=True, description='User last name'),
        'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
        'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
    })

    user_update_model = api.model('UserUpdate', {
        'email': fields.String(description='User email address'),
        'password': fields.String(description='User password'),
        'first_name': fields.String(description='User first name'),
        'last_name': fields.String(description='User last name')
    })

    # Place models
    place_model = api.model('Place', {
        'id': fields.String(readonly=True, description='Place unique identifier'),
        'city_id': fields.String(required=True, description='City identifier'),
        'user_id': fields.String(required=True, description='Owner user identifier'),
        'name': fields.String(required=True, description='Place name'),
        'description': fields.String(description='Place description'),
        'number_rooms': fields.Integer(description='Number of rooms'),
        'number_bathrooms': fields.Integer(description='Number of bathrooms'),
        'max_guest': fields.Integer(description='Maximum number of guests'),
        'price_by_night': fields.Integer(description='Price per night'),
        'latitude': fields.Float(description='Latitude coordinate'),
        'longitude': fields.Float(description='Longitude coordinate'),
        'amenity_ids': fields.List(fields.String, description='List of amenity IDs'),
        'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
        'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
    })

    place_update_model = api.model('PlaceUpdate', {
        'city_id': fields.String(description='City identifier'),
        'user_id': fields.String(description='Owner user identifier'),
        'name': fields.String(description='Place name'),
        'description': fields.String(description='Place description'),
        'number_rooms': fields.Integer(description='Number of rooms'),
        'number_bathrooms': fields.Integer(description='Number of bathrooms'),
        'max_guest': fields.Integer(description='Maximum number of guests'),
        'price_by_night': fields.Integer(description='Price per night'),
        'latitude': fields.Float(description='Latitude coordinate'),
        'longitude': fields.Float(description='Longitude coordinate')
    })

    # Review models
    review_model = api.model('Review', {
        'id': fields.String(readonly=True, description='Review unique identifier'),
        'place_id': fields.String(required=True, description='Place identifier'),
        'user_id': fields.String(required=True, description='Reviewer user identifier'),
        'text': fields.String(required=True, description='Review text'),
        'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
        'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
    })

    review_update_model = api.model('ReviewUpdate', {
        'place_id': fields.String(description='Place identifier'),
        'user_id': fields.String(description='Reviewer user identifier'),
        'text': fields.String(description='Review text')
    })

    # Amenity models
    amenity_model = api.model('Amenity', {
        'id': fields.String(readonly=True, description='Amenity unique identifier'),
        'name': fields.String(required=True, description='Amenity name'),
        'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
        'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
    })

    amenity_update_model = api.model('AmenityUpdate', {
        'name': fields.String(description='Amenity name')
    })

    # Error models
    error_model = api.model('Error', {
        'message': fields.String(description='Error message'),
        'status': fields.Integer(description='HTTP status code')
    })

    # Success models
    success_model = api.model('Success', {
        'message': fields.String(description='Success message'),
        'status': fields.Integer(description='HTTP status code')
    })

    return {
        'user': user_model,
        'user_response': user_response_model,
        'user_update': user_update_model,
        'place': place_model,
        'place_update': place_update_model,
        'review': review_model,
        'review_update': review_update_model,
        'amenity': amenity_model,
        'amenity_update': amenity_update_model,
        'error': error_model,
        'success': success_model
    }