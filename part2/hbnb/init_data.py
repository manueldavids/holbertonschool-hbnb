#!/usr/bin/env python3
"""
Data initialization script for HBnB application
This script creates sample data for testing the API
"""

from app import create_app
from app.services import hbnb_facade

def init_sample_data():
    """Initialize sample data for testing"""
    print("Initializing sample data...")
    
    # Create sample users
    users_data = [
        {
            'email': 'john@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe'
        },
        {
            'email': 'jane@example.com',
            'password': 'password456',
            'first_name': 'Jane',
            'last_name': 'Smith'
        },
        {
            'email': 'bob@example.com',
            'password': 'password789',
            'first_name': 'Bob',
            'last_name': 'Johnson'
        }
    ]
    
    created_users = []
    for user_data in users_data:
        user = hbnb_facade.create_user(user_data)
        if user:
            created_users.append(user)
            print(f"Created user: {user.email}")
        else:
            print(f"Failed to create user: {user_data['email']}")
    
    # Create sample amenities
    amenities_data = [
        {'name': 'WiFi'},
        {'name': 'Air Conditioning'},
        {'name': 'Kitchen'},
        {'name': 'Free Parking'},
        {'name': 'Pool'},
        {'name': 'Gym'},
        {'name': 'Pet Friendly'},
        {'name': 'Balcony'}
    ]
    
    created_amenities = []
    for amenity_data in amenities_data:
        amenity = hbnb_facade.create_amenity(amenity_data)
        if amenity:
            created_amenities.append(amenity)
            print(f"Created amenity: {amenity.name}")
        else:
            print(f"Failed to create amenity: {amenity_data['name']}")
    
    # Create sample places
    places_data = [
        {
            'name': 'Cozy Downtown Apartment',
            'description': 'Beautiful apartment in the heart of downtown',
            'city_id': 'city_001',
            'user_id': created_users[0].id,
            'number_rooms': 2,
            'number_bathrooms': 1,
            'max_guest': 4,
            'price_by_night': 100,
            'latitude': 40.7128,
            'longitude': -74.0060
        },
        {
            'name': 'Luxury Beach House',
            'description': 'Stunning beachfront property with ocean views',
            'city_id': 'city_002',
            'user_id': created_users[1].id,
            'number_rooms': 4,
            'number_bathrooms': 3,
            'max_guest': 8,
            'price_by_night': 300,
            'latitude': 34.0522,
            'longitude': -118.2437
        },
        {
            'name': 'Mountain Cabin Retreat',
            'description': 'Peaceful cabin surrounded by nature',
            'city_id': 'city_003',
            'user_id': created_users[2].id,
            'number_rooms': 3,
            'number_bathrooms': 2,
            'max_guest': 6,
            'price_by_night': 150,
            'latitude': 39.7392,
            'longitude': -104.9903
        }
    ]
    
    created_places = []
    for place_data in places_data:
        place = hbnb_facade.create_place(place_data)
        if place:
            created_places.append(place)
            print(f"Created place: {place.name}")
        else:
            print(f"Failed to create place: {place_data['name']}")
    
    # Add amenities to places
    if created_places and created_amenities:
        # Add WiFi and AC to all places
        for place in created_places:
            hbnb_facade.add_amenity_to_place(place.id, created_amenities[0].id)  # WiFi
            hbnb_facade.add_amenity_to_place(place.id, created_amenities[1].id)  # AC
            print(f"Added WiFi and AC to {place.name}")
        
        # Add kitchen to first place
        hbnb_facade.add_amenity_to_place(created_places[0].id, created_amenities[2].id)
        print(f"Added Kitchen to {created_places[0].name}")
        
        # Add pool to second place
        hbnb_facade.add_amenity_to_place(created_places[1].id, created_amenities[4].id)
        print(f"Added Pool to {created_places[1].name}")
    
    # Create sample reviews
    reviews_data = [
        {
            'place_id': created_places[0].id,
            'user_id': created_users[1].id,
            'text': 'Great location and very clean apartment!'
        },
        {
            'place_id': created_places[0].id,
            'user_id': created_users[2].id,
            'text': 'Perfect for a weekend getaway.'
        },
        {
            'place_id': created_places[1].id,
            'user_id': created_users[0].id,
            'text': 'Amazing beach views and luxurious amenities!'
        }
    ]
    
    for review_data in reviews_data:
        review = hbnb_facade.create_review(review_data)
        if review:
            print(f"Created review for place {review_data['place_id']}")
        else:
            print(f"Failed to create review for place {review_data['place_id']}")
    
    # Print statistics
    stats = hbnb_facade.get_statistics()
    print("\n=== Final Statistics ===")
    print(f"Total Users: {stats['total_users']}")
    print(f"Total Places: {stats['total_places']}")
    print(f"Total Reviews: {stats['total_reviews']}")
    print(f"Total Amenities: {stats['total_amenities']}")
    print("\nSample data initialization completed!")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        init_sample_data() 