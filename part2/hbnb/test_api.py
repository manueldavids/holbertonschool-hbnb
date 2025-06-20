#!/usr/bin/env python3
"""
Basic API testing script
This script tests the main API endpoints
"""

import requests
import json
import time

BASE_URL = 'http://localhost:5000/api/v1'

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get('http://localhost:5000/health')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_users_api():
    """Test users API endpoints"""
    print("=== Testing Users API ===")
    
    # Test create user
    print("1. Creating user...")
    user_data = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    response = requests.post(f'{BASE_URL}/users/', json=user_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        user = response.json()
        user_id = user['id']
        print(f"Created user with ID: {user_id}")
    else:
        print(f"Error: {response.json()}")
        return
    
    # Test get user
    print("\n2. Getting user...")
    response = requests.get(f'{BASE_URL}/users/{user_id}')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"User: {response.json()}")
    else:
        print(f"Error: {response.json()}")
    
    # Test update user
    print("\n3. Updating user...")
    update_data = {'first_name': 'Updated'}
    response = requests.put(f'{BASE_URL}/users/{user_id}', json=update_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Updated user: {response.json()}")
    else:
        print(f"Error: {response.json()}")
    
    # Test get all users
    print("\n4. Getting all users...")
    response = requests.get(f'{BASE_URL}/users/')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        users = response.json()
        print(f"Total users: {len(users)}")
    else:
        print(f"Error: {response.json()}")
    
    print()

def test_places_api():
    """Test places API endpoints"""
    print("=== Testing Places API ===")
    
    # First, create a user for the place
    user_data = {
        'email': 'placeowner@example.com',
        'password': 'password123',
        'first_name': 'Place',
        'last_name': 'Owner'
    }
    response = requests.post(f'{BASE_URL}/users/', json=user_data)
    if response.status_code == 201:
        user = response.json()
        user_id = user['id']
    else:
        print("Failed to create user for place testing")
        return
    
    # Test create place
    print("1. Creating place...")
    place_data = {
        'name': 'Test Place',
        'description': 'A test place for API testing',
        'city_id': 'test_city',
        'user_id': user_id,
        'number_rooms': 2,
        'number_bathrooms': 1,
        'max_guest': 4,
        'price_by_night': 100
    }
    response = requests.post(f'{BASE_URL}/places/', json=place_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        place = response.json()
        place_id = place['id']
        print(f"Created place with ID: {place_id}")
    else:
        print(f"Error: {response.json()}")
        return
    
    # Test get place
    print("\n2. Getting place...")
    response = requests.get(f'{BASE_URL}/places/{place_id}')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Place: {response.json()}")
    else:
        print(f"Error: {response.json()}")
    
    # Test search places
    print("\n3. Searching places...")
    response = requests.get(f'{BASE_URL}/places/search?name=Test')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        places = response.json()
        print(f"Found {len(places)} places")
    else:
        print(f"Error: {response.json()}")
    
    print()

def test_amenities_api():
    """Test amenities API endpoints"""
    print("=== Testing Amenities API ===")
    
    # Test create amenity
    print("1. Creating amenity...")
    amenity_data = {'name': 'Test Amenity'}
    response = requests.post(f'{BASE_URL}/amenities/', json=amenity_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        amenity = response.json()
        amenity_id = amenity['id']
        print(f"Created amenity with ID: {amenity_id}")
    else:
        print(f"Error: {response.json()}")
        return
    
    # Test get amenity
    print("\n2. Getting amenity...")
    response = requests.get(f'{BASE_URL}/amenities/{amenity_id}')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Amenity: {response.json()}")
    else:
        print(f"Error: {response.json()}")
    
    # Test search amenities
    print("\n3. Searching amenities...")
    response = requests.get(f'{BASE_URL}/amenities/search?name=Test')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        amenities = response.json()
        print(f"Found {len(amenities)} amenities")
    else:
        print(f"Error: {response.json()}")
    
    print()

def test_reviews_api():
    """Test reviews API endpoints"""
    print("=== Testing Reviews API ===")
    
    # First, create a user and place for the review
    user_data = {
        'email': 'reviewer@example.com',
        'password': 'password123',
        'first_name': 'Reviewer',
        'last_name': 'User'
    }
    response = requests.post(f'{BASE_URL}/users/', json=user_data)
    if response.status_code == 201:
        user = response.json()
        user_id = user['id']
    else:
        print("Failed to create user for review testing")
        return
    
    place_data = {
        'name': 'Review Test Place',
        'description': 'A place for review testing',
        'city_id': 'test_city',
        'user_id': user_id,
        'number_rooms': 1,
        'number_bathrooms': 1,
        'max_guest': 2,
        'price_by_night': 50
    }
    response = requests.post(f'{BASE_URL}/places/', json=place_data)
    if response.status_code == 201:
        place = response.json()
        place_id = place['id']
    else:
        print("Failed to create place for review testing")
        return
    
    # Test create review
    print("1. Creating review...")
    review_data = {
        'place_id': place_id,
        'user_id': user_id,
        'text': 'This is a test review for API testing'
    }
    response = requests.post(f'{BASE_URL}/reviews/', json=review_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        review = response.json()
        review_id = review['id']
        print(f"Created review with ID: {review_id}")
    else:
        print(f"Error: {response.json()}")
        return
    
    # Test get review
    print("\n2. Getting review...")
    response = requests.get(f'{BASE_URL}/reviews/{review_id}')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Review: {response.json()}")
    else:
        print(f"Error: {response.json()}")
    
    print()

def main():
    """Run all tests"""
    print("Starting API tests...")
    print("Make sure the server is running on http://localhost:5000")
    print()
    
    try:
        test_health_check()
        test_users_api()
        test_places_api()
        test_amenities_api()
        test_reviews_api()
        
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
        print("Make sure the Flask application is running on http://localhost:5000")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == '__main__':
    main() 