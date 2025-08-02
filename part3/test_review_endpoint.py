#!/usr/bin/env python3
"""
Script to test the review endpoint logic.
"""

from app import create_app, db
from app.models.user import User
from flask_jwt_extended import create_access_token, get_jwt_identity
import jwt

def test_review_logic():
    """Test the review endpoint logic."""
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
        
        # Simulate the get_current_user function
        try:
            # Decode the token to get the user ID
            decoded = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user_id = decoded.get('sub')
            print(f"🔍 Token user ID: {current_user_id}")
            
            # Try to get the user by ID
            user_from_db = User.get_by_id(current_user_id)
            if user_from_db:
                print(f"✅ User found in DB: {user_from_db}")
            else:
                print(f"❌ User not found in DB with ID: {current_user_id}")
                
                # Check if there's a database session issue
                print("🔍 Checking database session...")
                all_users = User.get_all_users()
                print(f"📋 All users in DB: {len(all_users)}")
                for u in all_users:
                    print(f"   - {u.id}: {u.email}")
                    
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_review_logic() 