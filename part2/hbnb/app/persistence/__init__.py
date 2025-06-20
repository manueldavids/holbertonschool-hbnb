from typing import List
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class UserRepository(InMemoryRepository):
    def get_by_email(self, email: str):
        """Get user by email address"""
        return self.get_by_attribute('email', email)
    
    def authenticate(self, email: str, password: str):
        """Authenticate user with email and password"""
        user = self.get_by_email(email)
        if user and user.password == password:  # In real app, use proper hashing
            return user
        return None

class PlaceRepository(InMemoryRepository):
    def get_by_user_id(self, user_id: str) -> List[Place]:
        """Get all places owned by a specific user"""
        return self.get_by_attributes({'user_id': user_id})
    
    def get_by_city_id(self, city_id: str) -> List[Place]:
        """Get all places in a specific city"""
        return self.get_by_attributes({'city_id': city_id})
    
    def search_by_name(self, name: str) -> List[Place]:
        """Search places by name (partial match)"""
        matching_places = []
        for place in self._storage.values():
            if name.lower() in place.name.lower():
                matching_places.append(place)
        return matching_places

class ReviewRepository(InMemoryRepository):
    def get_by_place_id(self, place_id: str) -> List[Review]:
        """Get all reviews for a specific place"""
        return self.get_by_attributes({'place_id': place_id})
    
    def get_by_user_id(self, user_id: str) -> List[Review]:
        """Get all reviews written by a specific user"""
        return self.get_by_attributes({'user_id': user_id})

class AmenityRepository(InMemoryRepository):
    def get_by_name(self, name: str):
        """Get amenity by exact name"""
        return self.get_by_attribute('name', name)
    
    def search_by_name(self, name: str) -> List[Amenity]:
        """Search amenities by name (partial match)"""
        matching_amenities = []
        for amenity in self._storage.values():
            if name.lower() in amenity.name.lower():
                matching_amenities.append(amenity)
        return matching_amenities