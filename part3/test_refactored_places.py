#!/usr/bin/env python3
"""
Test script for refactored Places endpoints.
"""

from app import create_app

def test_refactored_places():
    """Test refactored places endpoints."""
    app = create_app('development')
    
    with app.test_client() as client:
        print("Testing Refactored Places Endpoints")
        print("=" * 40)
        
        # Test GET /places (public)
        print("\n1. Testing GET /api/v1/places/ (public)")
        response = client.get('/api/v1/places/')
        print(f"Status: {response.status_code}")
        print(f"Response: {response.get_json()}")
        
        # Test POST /places without auth (should fail)
        print("\n2. Testing POST /api/v1/places/ without auth")
        response = client.post('/api/v1/places/', 
                             json={'name': 'Test Place'})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.get_json()}")
        
        # Test with invalid data
        print("\n3. Testing POST /api/v1/places/ with invalid data")
        response = client.post('/api/v1/places/', 
                             json={'price_per_night': -100})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.get_json()}")
        
        print("\nRefactored places test completed!")

if __name__ == "__main__":
    test_refactored_places() 