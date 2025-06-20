from flask import request, jsonify
from flask_restx import Namespace, Resource
from app.services import hbnb_facade
from app.api.v1.models import create_api_models

# Create namespace
api = Namespace('users', description='User operations')

# Get API models
models = create_api_models(api)

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(models['user_response'])
    def get(self):
        """List all users"""
        try:
            users = hbnb_facade.get_all_users()
            return [user.to_dict() for user in users], 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('create_user')
    @api.expect(models['user'])
    @api.marshal_with(models['user_response'], code=201)
    def post(self):
        """Create a new user"""
        try:
            data = request.get_json()
            if not data:
                api.abort(400, "No data provided")
            
            user = hbnb_facade.create_user(data)
            if user:
                return user.to_dict(), 201
            else:
                api.abort(400, "Failed to create user")
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(models['user_response'])
    def get(self, user_id):
        """Get a user by ID"""
        try:
            user = hbnb_facade.get_user(user_id)
            if user:
                return user.to_dict(), 200
            else:
                api.abort(404, "User not found")
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('update_user')
    @api.expect(models['user_update'])
    @api.marshal_with(models['user_response'])
    def put(self, user_id):
        """Update a user"""
        try:
            data = request.get_json()
            if not data:
                api.abort(400, "No data provided")
            
            success = hbnb_facade.update_user(user_id, data)
            if success:
                user = hbnb_facade.get_user(user_id)
                return user.to_dict(), 200
            else:
                api.abort(404, "User not found")
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @api.doc('delete_user')
    @api.response(204, 'User deleted')
    def delete(self, user_id):
        """Delete a user"""
        try:
            success = hbnb_facade.delete_user(user_id)
            if success:
                return '', 204
            else:
                api.abort(404, "User not found")
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

@api.route('/login')
class UserLogin(Resource):
    @api.doc('user_login')
    @api.expect(api.model('Login', {
        'email': fields.String(required=True, description='User email'),
        'password': fields.String(required=True, description='User password')
    }))
    @api.marshal_with(models['user_response'])
    def post(self):
        """Authenticate user"""
        try:
            data = request.get_json()
            if not data or 'email' not in data or 'password' not in data:
                api.abort(400, "Email and password are required")
            
            user = hbnb_facade.authenticate_user(data['email'], data['password'])
            if user:
                return user.to_dict(), 200
            else:
                api.abort(401, "Invalid credentials")
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")