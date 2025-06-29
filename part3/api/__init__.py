"""
API blueprint for the HBnB application.
Registers all API namespaces and routes.
"""

from flask import Blueprint
from flask_restx import Api

# Create the main API blueprint
api_bp = Blueprint('api', __name__)

# Create the Flask-RESTX API instance
api = Api(
    api_bp,
    title='HBnB API',
    version='1.0',
    description='A RESTful API for HBnB application',
    doc='/docs'
)

# Import and register namespaces
from api.v1.auth import api as auth_api
from api.v1.users import api as users_api
from api.v1.places import api as places_api
from api.v1.reviews import api as reviews_api
from api.v1.admin import api as admin_api

api.add_namespace(auth_api, path='/auth')
api.add_namespace(users_api, path='/users')
api.add_namespace(places_api, path='/places')
api.add_namespace(reviews_api, path='/reviews')
api.add_namespace(admin_api, path='/admin')
