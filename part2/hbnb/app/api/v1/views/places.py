from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import hbnb_facade
from app.api.v1.models import create_api_models

# Create namespace
api = Namespace('places', description='Place operations')

# Get API models
models = create_api_models(api)

@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(models['place'])
    def get(self):
        """List all places"""
        try:
            places = hbnb_facade.get_all_places()
            return [place.to_dict() for place in places], 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('create_place')
    @api.expect(models['place'])
    @api.marshal_with(models['place'], code=201)
    def post(self):
        """Create a new place"""
        try:
            data = request.get_json()
            if not data:
                api.abort(400, "No data provided")
            
            place = hbnb_facade.create_place(data)
            if place:
                return place.to_dict(), 201
            else:
                api.abort(400, "Failed to create place")
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.marshal_with(models['place'])
    def get(self, place_id):
        """Get a place by ID"""
        try:
            place = hbnb_facade.get_place(place_id)
            if place:
                return place.to_dict(), 200
            else:
                api.abort(404, "Place not found")
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('update_place')
    @api.expect(models['place_update'])
    @api.marshal_with(models['place'])
    def put(self, place_id):
        """Update a place"""
        try:
            data = request.get_json()
            if not data:
                api.abort(400, "No data provided")
            
            success = hbnb_facade.update_place(place_id, data)
            if success:
                place = hbnb_facade.get_place(place_id)
                return place.to_dict(), 200
            else:
                api.abort(404, "Place not found")
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('delete_place')
    @api.response(204, 'Place deleted')
    def delete(self, place_id):
        """Delete a place"""
        try:
            success = hbnb_facade.delete_place(place_id)
            if success:
                return '', 204
            else:
                api.abort(404, "Place not found")
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

@api.route('/search')
class PlaceSearch(Resource):
    @api.doc('search_places')
    @api.param('name', 'Place name to search for')
    @api.marshal_list_with(models['place'])
    def get(self):
        """Search places by name"""
        try:
            name = request.args.get('name')
            if not name:
                api.abort(400, "Name parameter is required")
            
            places = hbnb_facade.search_places(name)
            return [place.to_dict() for place in places], 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

@api.route('/user/<string:user_id>')
@api.param('user_id', 'The user identifier')
class UserPlaces(Resource):
    @api.doc('get_user_places')
    @api.marshal_list_with(models['place'])
    def get(self, user_id):
        """Get all places owned by a user"""
        try:
            places = hbnb_facade.get_places_by_user(user_id)
            return [place.to_dict() for place in places], 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

@api.route('/<string:place_id>/amenities/<string:amenity_id>')
@api.param('place_id', 'The place identifier')
@api.param('amenity_id', 'The amenity identifier')
class PlaceAmenity(Resource):
    @api.doc('add_amenity_to_place')
    @api.response(200, 'Amenity added to place')
    def post(self, place_id, amenity_id):
        """Add amenity to place"""
        try:
            success = hbnb_facade.add_amenity_to_place(place_id, amenity_id)
            if success:
                return {'message': 'Amenity added to place'}, 200
            else:
                api.abort(400, "Failed to add amenity to place")
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('remove_amenity_from_place')
    @api.response(200, 'Amenity removed from place')
    def delete(self, place_id, amenity_id):
        """Remove amenity from place"""
        try:
            success = hbnb_facade.remove_amenity_from_place(place_id, amenity_id)
            if success:
                return {'message': 'Amenity removed from place'}, 200
            else:
                api.abort(400, "Failed to remove amenity from place")
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")