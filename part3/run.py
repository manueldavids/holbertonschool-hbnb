#!/usr/bin/env python3
"""
Simple script to run the Flask application.
"""

from app import create_app

if __name__ == '__main__':
    app = create_app('development')
    print(app.url_map)
    app.run(host='127.0.0.1', port=5000, debug=True) 