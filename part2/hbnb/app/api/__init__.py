from flask import Blueprint
from flask_restx import Api

# Create the API blueprint
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Create the API instance
api = Api(api_v1, 
          version='1.0', 
          title='HBnB API',
          description='A RESTful API for HBnB application',
          doc='/docs/')

# Import and register namespaces
from app.api.v1.views.users import api as users_ns
from app.api.v1.views.places import api as places_ns
from app.api.v1.views.reviews import api as reviews_ns
from app.api.v1.views.amenities import api as amenities_ns

# Add namespaces to API
api.add_namespace(users_ns, path='/users')
api.add_namespace(places_ns, path='/places')
api.add_namespace(reviews_ns, path='/reviews')
api.add_namespace(amenities_ns, path='/amenities')