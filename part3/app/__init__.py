"""
Application Factory for the HBNB Flask application.
Implements the factory pattern with configuration handling.
"""

import os
import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

# Import configuration
from app.config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(config_name=None):
    """
    Application Factory function.

    Args:
        config_name (str): Configuration name ('development', 'testing',
            'production') If None, uses FLASK_ENV environment variable or
            'default'

    Returns:
        Flask: Configured Flask application instance

    Raises:
        ValueError: If invalid configuration name is provided
        RuntimeError: If required environment variables are missing
    """
    # INPUT VALUES WE ARE RECEIVING
    # Determine configuration to use
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    # Validate configuration name
    if config_name not in config:
        raise ValueError(
            f"Invalid configuration name: {config_name}. "
            f"Available: {list(config.keys())}"
        )

    # Get configuration class
    config_class = config[config_name]

    # VALUES WE ARE GOING TO RETURN
    # Create Flask application
    app = Flask(__name__)

    # Initialize Flask-Bcrypt
    bcrypt.init_app(app)

    # WE HANDLE EXCEPTIONS
    try:
        # Apply configuration
        app.config.from_object(config_class)

        # Validate required environment variables for production
        if config_name == 'production':
            required_vars = [
                'SECRET_KEY', 'DATABASE_URL', 'JWT_SECRET_KEY'
            ]
            missing_vars = [
                var for var in required_vars if not os.environ.get(var)
            ]
            if missing_vars:
                raise RuntimeError(
                    f"Missing required environment variables: {missing_vars}"
                )
    except Exception as e:
        # Log the error and re-raise
        logging.error(f"Failed to configure application: {str(e)}")
        raise

    # DIFFERENT WAYS TO HANDLE THE PROCESS WITH PREVIOUSLY VERIFIED VALUES

    # Method 1: Conditional initialization based on configuration
    _initialize_extensions(app, config_name)

    # Import models so Alembic can detect them
    from app.models import user


    # Remove all Blueprint registration and usage. Only use Flask-RESTX Api for endpoint registration. Clean up imports and initialization accordingly. Remove _register_blueprints and related logic.

    # Method 3: Logging configuration and error handling
    _setup_error_handlers(app, config_name)

    # Import and register the Api here to avoid circular import
    from api import api_bp
    app.register_blueprint(api_bp)
    return app


def _initialize_extensions(app, config_name):
    """
    Initialize Flask extensions based on configuration.

    Args:
        app (Flask): Flask application instance
        config_name (str): Configuration name
    """
    try:
        # Initialize database
        db.init_app(app)
        migrate.init_app(app, db)

        # Initialize JWT
        jwt.init_app(app)

        # Initialize CORS
        CORS(app)

        # Initialize Swagger UI for development and testing
        if config_name in ['development', 'testing']:
            from flask_swagger_ui import get_swaggerui_blueprint
            swagger_blueprint = get_swaggerui_blueprint(
                app.config.get('OPENAPI_SWAGGER_UI_PATH', '/swagger-ui'),
                '/api/v1/swagger.json',  # <-- Correct spec URL
                config={
                    'app_name': app.config.get('API_TITLE', 'HBNB API')
                }
            )
            # app.register_blueprint(
            #     swagger_blueprint,
            #     url_prefix=app.config.get(
            #         'OPENAPI_SWAGGER_UI_PATH', '/swagger-ui'
            #     )
            # )
    except Exception as e:
        logging.error(f"Failed to initialize extensions: {str(e)}")
        raise


# Remove all Blueprint registration and usage. Only use Flask-RESTX Api for endpoint registration. Clean up imports and initialization accordingly. Remove _register_blueprints and related logic.


def _setup_error_handlers(app, config_name):
    """
    Setup error handlers and logging configuration.

    Args:
        app (Flask): Flask application instance
        config_name (str): Configuration name
    """
    try:
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, app.config.get('LOG_LEVEL', 'INFO')),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Error handlers
        @app.errorhandler(404)
        def not_found(error):
            return jsonify({
                'error': 'Not Found',
                'message': 'The requested resource was not found'
            }), 404

        @app.errorhandler(500)
        def internal_error(error):
            db.session.rollback()
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred'
            }), 500

        @app.errorhandler(400)
        def bad_request(error):
            return jsonify({
                'error': 'Bad Request',
                'message': 'Invalid request data'
            }), 400

        # Development-specific error handling
        if config_name == 'development':
            @app.errorhandler(Exception)
            def handle_exception(e):
                app.logger.error(f"Unhandled exception: {str(e)}")
                return jsonify({
                    'error': 'Internal Server Error',
                    'message': str(e),
                    'type': type(e).__name__
                }), 500
    except Exception as e:
        logging.error(f"Failed to setup error handlers: {str(e)}")
        raise


# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'error': 'Token Expired',
        'message': 'The token has expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': 'Invalid Token',
        'message': 'The token is invalid'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': 'Missing Token',
        'message': 'Request does not contain an access token'
    }), 401
