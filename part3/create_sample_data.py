#!/usr/bin/env python3
"""
Script to create sample data for HBnB application.
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import user, place, amenity, review
from app.services.facade import Facade

def create_sample_data():
    """Create sample data for testing."""
    try:
        # Create Flask app
        app = create_app('development')
        facade = Facade()
        
        # Create application context
        with app.app_context():
            print("🔧 Creating sample data...")
            
            # Create a test user if it doesn't exist
            test_user = facade.get_user_by_email('test@example.com')
            if not test_user:
                print("❌ Test user not found. Please create a user first.")
                return False
            
            # Create sample places
            sample_places = [
                {
                    'name': 'Beautiful Beach House',
                    'description': 'Stunning beachfront property with ocean views',
                    'address': '123 Beach Road, Malibu, CA',
                    'price_per_night': 250.0,
                    'max_guests': 6,
                    'latitude': 34.0259,
                    'longitude': -118.7798,
                    'owner_id': test_user['id']
                },
                {
                    'name': 'Cozy Mountain Cabin',
                    'description': 'Peaceful cabin in the mountains with hiking trails',
                    'address': '456 Mountain View, Aspen, CO',
                    'price_per_night': 180.0,
                    'max_guests': 4,
                    'latitude': 39.1911,
                    'longitude': -106.8175,
                    'owner_id': test_user['id']
                },
                {
                    'name': 'Modern Downtown Apartment',
                    'description': 'Luxury apartment in the heart of the city',
                    'address': '789 City Center, New York, NY',
                    'price_per_night': 300.0,
                    'max_guests': 2,
                    'latitude': 40.7128,
                    'longitude': -74.0060,
                    'owner_id': test_user['id']
                },
                {
                    'name': 'Rustic Farmhouse',
                    'description': 'Charming farmhouse with beautiful gardens',
                    'address': '321 Country Lane, Napa, CA',
                    'price_per_night': 200.0,
                    'max_guests': 8,
                    'latitude': 38.2975,
                    'longitude': -122.2869,
                    'owner_id': test_user['id']
                }
            ]
            
            created_places = []
            for place_data in sample_places:
                try:
                    place = facade.create_place(place_data, test_user['id'])
                    if place:
                        created_places.append(place)
                        print(f"✅ Created place: {place_data['name']}")
                    else:
                        print(f"❌ Failed to create place: {place_data['name']}")
                except Exception as e:
                    print(f"❌ Error creating place {place_data['name']}: {e}")
            
            print(f"\n🎉 Created {len(created_places)} sample places!")
            return True
            
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Creating Sample Data for HBnB...")
    print("=" * 40)
    
    if create_sample_data():
        print("=" * 40)
        print("🎉 Sample data creation completed!")
    else:
        print("=" * 40)
        print("💥 Sample data creation failed!")
        sys.exit(1) 