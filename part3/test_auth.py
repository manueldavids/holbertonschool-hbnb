#!/usr/bin/env python3
"""
Script to test the get_current_user function.
"""

from app import create_app, db
from app.models.user import User
from flask_jwt_extended import create_access_token
import jwt

def test_get_current_user():
    """Test the get_current_user function."""
    app = create_app()
    with app.app_context():
        # Get a user from the database
        user = User.get_by_email("newuser@example.com")
        if not user:
            print("❌ User not found")
            return
        
        print(f"✅ Found user: {user}")
        print(f"   ID: {user.id}")
        
        # Create a JWT token for this user
        token = create_access_token(identity=user.id)
        print(f"🔑 Created token: {token}")
        
        # Decode the token to verify
        try:
            decoded = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            print(f"🔍 Decoded token identity: {decoded.get('sub')}")
            print(f"🔍 User ID from database: {user.id}")
            print(f"🔍 Match: {decoded.get('sub') == user.id}")
        except Exception as e:
            print(f"❌ Error decoding token: {e}")

if __name__ == "__main__":
    test_get_current_user() 