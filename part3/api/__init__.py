"""
API blueprint for the HBnB application.
Registers all API namespaces and routes.
"""

# API initialization for the HBnB application using Flask-RESTX only
from flask_restx import Api
from .v1.auth import api as auth_ns
from .v1.users import api as users_ns
from .v1.admin import api as admin_ns
from .v1.places import api as places_ns
from .v1.reviews import api as reviews_ns

# Create the main API object (no Blueprint)
api = Api(
    title='HBnB API',
    version='1.0',
    description='REST API for the HBnB application',
    doc='/docs'  # Swagger UI available at /docs
)

api.add_namespace(auth_ns, path='/auth')
api.add_namespace(users_ns, path='/users')
api.add_namespace(admin_ns, path='/admin')
api.add_namespace(places_ns, path='/places')
api.add_namespace(reviews_ns, path='/reviews')

