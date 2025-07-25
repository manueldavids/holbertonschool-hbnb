"""
Configuration module for the HBNB Flask application.
Handles different environment configurations.
"""

import os
from datetime import timedelta


class BaseConfig:
    """Base configuration class with common settings."""

    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        'dev-secret-key-change-in-production'

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///instance/hbnb_dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # API configuration
    API_TITLE = 'HBNB API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_SWAGGER_UI_PATH = '/swagger-ui'
    OPENAPI_SWAGGER_UI_URL = \
        'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

    # Pagination
    ITEMS_PER_PAGE = 20

    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'

    # CORS configuration
    CORS_HEADERS = 'Content-Type'

    # Logging configuration
    LOG_LEVEL = 'INFO'


class DevelopmentConfig(BaseConfig):
    """Development configuration with debug enabled."""

    DEBUG = True
    TESTING = False

    # Development database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///instance/hbnb_dev.db'

    # Development logging
    LOG_LEVEL = 'DEBUG'


class TestingConfig(BaseConfig):
    """Testing configuration with testing mode enabled."""

    DEBUG = False
    TESTING = True

    # Testing database
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///instance/hbnb_test.db'

    # Disable CSRF protection for testing
    WTF_CSRF_ENABLED = False

    # Testing logging
    LOG_LEVEL = 'INFO'


class ProductionConfig(BaseConfig):
    """Production configuration with security settings."""

    DEBUG = False
    TESTING = False

    # Production database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # Production logging
    LOG_LEVEL = 'WARNING'

    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


def get_config_dict():
    """Get configuration dictionary mapping names to classes."""
    return {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
    }


def get_config(config_name):
    """
    Get configuration class by name.

    Args:
        config_name (str): Configuration name

    Returns:
        class: Configuration class

    Raises:
        ValueError: If configuration name is invalid
    """
    config_dict = get_config_dict()
    if config_name not in config_dict:
        raise ValueError(
            f"Invalid configuration name: {config_name}. "
            f"Available: {list(config_dict.keys())}"
        )
    return config_dict[config_name]


def get_available_configs():
    """Get list of available configuration names."""
    return list(get_config_dict().keys())


# Backward compatibility - keep the original config dict
config = get_config_dict()
