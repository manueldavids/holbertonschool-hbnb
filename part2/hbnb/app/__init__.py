from flask import Flask
from flask_restx import Api
from config import config

def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize API
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1)
    
    # Add error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'message': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'message': 'Internal server error'}, 500
    
    # Add health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'HBnB API is running'}, 200
    
    return app