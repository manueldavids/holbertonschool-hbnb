#!/usr/bin/env python3
"""
Script to check if a user exists in the database.
"""

from app import create_app, db
from app.models.user import User

def check_user(user_id):
    """Check if a user exists by ID."""
    app = create_app()
    with app.app_context():
        user = User.get_by_id(user_id)
        if user:
            print(f"✅ User found: {user}")
            print(f"   ID: {user.id}")
            print(f"   Email: {user.email}")
            print(f"   Name: {user.first_name} {user.last_name}")
        else:
            print(f"❌ User not found with ID: {user_id}")
        
        # Also check all users
        all_users = User.get_all_users()
        print(f"\n📋 All users in database ({len(all_users)}):")
        for u in all_users:
            print(f"   - {u.id}: {u.email}")

if __name__ == "__main__":
    user_id = "e049f2fd-664a-4727-a546-0d1f18500c77"  # From the registration response
    check_user(user_id) 