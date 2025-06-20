from flask import request
from flask_restx import Namespace, Resource
from app.services import hbnb_facade
from app.api.v1.models import create_api_models

# Create namespace
api = Namespace('amenities', description='Amenity operations')

# Get API models
models = create_api_models(api)

@api.route('/')
class AmenityList(Resource):
    @api.doc('list_amenities')
    @api.marshal_list_with(models['amenity'])
    def get(self):
        """List all amenities"""
        try:
            amenities = hbnb_facade.get_all_amenities()
            return [amenity.to_dict() for amenity in amenities], 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('create_amenity')
    @api.expect(models['amenity'])
    @api.marshal_with(models['amenity'], code=201)
    def post(self):
        """Create a new amenity"""
        try:
            data = request.get_json()
            if not data:
                api.abort(400, "No data provided")
            
            amenity = hbnb_facade.create_amenity(data)
            if amenity:
                return amenity.to_dict(), 201
            else:
                api.abort(400, "Failed to create amenity")
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(models['amenity'])
    def get(self, amenity_id):
        """Get an amenity by ID"""
        try:
            amenity = hbnb_facade.get_amenity(amenity_id)
            if amenity:
                return amenity.to_dict(), 200
            else:
                api.abort(404, "Amenity not found")
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('update_amenity')
    @api.expect(models['amenity_update'])
    @api.marshal_with(models['amenity'])
    def put(self, amenity_id):
        """Update an amenity"""
        try:
            data = request.get_json()
            if not data:
                api.abort(400, "No data provided")
            
            success = hbnb_facade.update_amenity(amenity_id, data)
            if success:
                amenity = hbnb_facade.get_amenity(amenity_id)
                return amenity.to_dict(), 200
            else:
                api.abort(404, "Amenity not found")
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('delete_amenity')
    @api.response(204, 'Amenity deleted')
    def delete(self, amenity_id):
        """Delete an amenity"""
        try:
            success = hbnb_facade.delete_amenity(amenity_id)
            if success:
                return '', 204
            else:
                api.abort(404, "Amenity not found")
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

@api.route('/search')
class AmenitySearch(Resource):
    @api.doc('search_amenities')
    @api.param('name', 'Amenity name to search for')
    @api.marshal_list_with(models['amenity'])
    def get(self):
        """Search amenities by name"""
        try:
            name = request.args.get('name')
            if not name:
                api.abort(400, "Name parameter is required")
            
            amenities = hbnb_facade.search_amenities(name)
            return [amenity.to_dict() for amenity in amenities], 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")