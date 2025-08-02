#!/usr/bin/env python3
"""
Script to test review creation directly.
"""

from app import create_app, db
from app.models.review import Review
from app.models.user import User
from app.models.place import Place
import uuid

def test_review_creation():
    """Test creating a review directly."""
    app = create_app()
    with app.app_context():
        try:
            # Get user and place
            user = User.get_by_email("newuser@example.com")
            place = Place.query.first()
            
            if not user:
                print("❌ User not found")
                return
                
            if not place:
                print("❌ Place not found")
                return
                
            print(f"✅ User: {user}")
            print(f"✅ Place: {place}")
            
            # Create review data
            review_data = {
                'id': str(uuid.uuid4()),
                'rating': 5,
                'comment': 'Amazing place! Beautiful views and very comfortable.',
                'place_id': place.id,
                'user_id': user.id
            }
            
            print(f"📝 Review data: {review_data}")
            
            # Create review instance
            review = Review(**review_data)
            print(f"✅ Review instance created: {review}")
            
            # Save to database
            db.session.add(review)
            db.session.commit()
            print(f"✅ Review saved to database")
            
            # Test to_dict method
            review_dict = review.to_dict()
            print(f"✅ Review to_dict: {review_dict}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_review_creation() 