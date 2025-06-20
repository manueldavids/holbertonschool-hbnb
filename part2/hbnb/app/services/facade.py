from app.persistence import UserRepository, PlaceRepository, ReviewRepository, AmenityRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from typing import List, Dict, Any, Optional

class HBnBFacade:
    def __init__(self):
        # Initialize repositories for each entity
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # ========== USER OPERATIONS ==========
    
    def create_user(self, user_data: Dict[str, Any]) -> Optional[User]:
        """Create a new user with validation"""
        try:
            # Validate required fields
            required_fields = ['email', 'password']
            for field in required_fields:
                if field not in user_data or not user_data[field]:
                    raise ValueError(f"Missing required field: {field}")
            
            # Check if email already exists
            if self.user_repo.get_by_email(user_data['email']):
                raise ValueError("Email already exists")
            
            # Create user
            user = User(**user_data)
            if self.user_repo.add(user):
                return user
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.user_repo.get(user_id)

    def get_all_users(self) -> List[User]:
        """Get all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> bool:
        """Update user with validation"""
        try:
            user = self.get_user(user_id)
            if not user:
                return False
            
            # Don't allow email change if new email already exists
            if 'email' in user_data and user_data['email'] != user.email:
                existing_user = self.user_repo.get_by_email(user_data['email'])
                if existing_user:
                    raise ValueError("Email already exists")
            
            return self.user_repo.update(user_id, user_data)
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    def delete_user(self, user_id: str) -> bool:
        """Delete user and all associated data"""
        try:
            user = self.get_user(user_id)
            if not user:
                return False
            
            # Delete user's places
            user_places = self.place_repo.get_by_user_id(user_id)
            for place in user_places:
                self.place_repo.delete(place.id)
            
            # Delete user's reviews
            user_reviews = self.review_repo.get_by_user_id(user_id)
            for review in user_reviews:
                self.review_repo.delete(review.id)
            
            # Delete user
            return self.user_repo.delete(user_id)
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        return self.user_repo.authenticate(email, password)

    # ========== PLACE OPERATIONS ==========
    
    def create_place(self, place_data: Dict[str, Any]) -> Optional[Place]:
        """Create a new place with validation"""
        try:
            # Validate required fields
            required_fields = ['name', 'user_id']
            for field in required_fields:
                if field not in place_data or not place_data[field]:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate user exists
            if not self.user_repo.exists(place_data['user_id']):
                raise ValueError("User does not exist")
            
            # Set default values
            place_data.setdefault('number_rooms', 0)
            place_data.setdefault('number_bathrooms', 0)
            place_data.setdefault('max_guest', 0)
            place_data.setdefault('price_by_night', 0)
            place_data.setdefault('amenity_ids', [])
            
            # Create place
            place = Place(**place_data)
            if self.place_repo.add(place):
                return place
            return None
        except Exception as e:
            print(f"Error creating place: {e}")
            return None

    def get_place(self, place_id: str) -> Optional[Place]:
        """Get place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self) -> List[Place]:
        """Get all places"""
        return self.place_repo.get_all()

    def get_places_by_user(self, user_id: str) -> List[Place]:
        """Get all places owned by a user"""
        return self.place_repo.get_by_user_id(user_id)

    def get_places_by_city(self, city_id: str) -> List[Place]:
        """Get all places in a city"""
        return self.place_repo.get_by_city_id(city_id)

    def search_places(self, name: str) -> List[Place]:
        """Search places by name"""
        return self.place_repo.search_by_name(name)

    def update_place(self, place_id: str, place_data: Dict[str, Any]) -> bool:
        """Update place with validation"""
        try:
            place = self.get_place(place_id)
            if not place:
                return False
            
            # Validate user exists if user_id is being updated
            if 'user_id' in place_data and not self.user_repo.exists(place_data['user_id']):
                raise ValueError("User does not exist")
            
            return self.place_repo.update(place_id, place_data)
        except Exception as e:
            print(f"Error updating place: {e}")
            return False

    def delete_place(self, place_id: str) -> bool:
        """Delete place and all associated reviews"""
        try:
            place = self.get_place(place_id)
            if not place:
                return False
            
            # Delete associated reviews
            place_reviews = self.review_repo.get_by_place_id(place_id)
            for review in place_reviews:
                self.review_repo.delete(review.id)
            
            return self.place_repo.delete(place_id)
        except Exception as e:
            print(f"Error deleting place: {e}")
            return False

    def add_amenity_to_place(self, place_id: str, amenity_id: str) -> bool:
        """Add amenity to place"""
        try:
            place = self.get_place(place_id)
            amenity = self.amenity_repo.get(amenity_id)
            
            if not place or not amenity:
                return False
            
            place.add_amenity(amenity_id)
            return True
        except Exception as e:
            print(f"Error adding amenity to place: {e}")
            return False

    def remove_amenity_from_place(self, place_id: str, amenity_id: str) -> bool:
        """Remove amenity from place"""
        try:
            place = self.get_place(place_id)
            if not place:
                return False
            
            place.remove_amenity(amenity_id)
            return True
        except Exception as e:
            print(f"Error removing amenity from place: {e}")
            return False

    # ========== REVIEW OPERATIONS ==========
    
    def create_review(self, review_data: Dict[str, Any]) -> Optional[Review]:
        """Create a new review with validation"""
        try:
            # Validate required fields
            required_fields = ['text', 'place_id', 'user_id']
            for field in required_fields:
                if field not in review_data or not review_data[field]:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate place and user exist
            if not self.place_repo.exists(review_data['place_id']):
                raise ValueError("Place does not exist")
            
            if not self.user_repo.exists(review_data['user_id']):
                raise ValueError("User does not exist")
            
            # Create review
            review = Review(**review_data)
            if self.review_repo.add(review):
                return review
            return None
        except Exception as e:
            print(f"Error creating review: {e}")
            return None

    def get_review(self, review_id: str) -> Optional[Review]:
        """Get review by ID"""
        return self.review_repo.get(review_id)

    def get_reviews_by_place(self, place_id: str) -> List[Review]:
        """Get all reviews for a place"""
        return self.review_repo.get_by_place_id(place_id)

    def get_reviews_by_user(self, user_id: str) -> List[Review]:
        """Get all reviews by a user"""
        return self.review_repo.get_by_user_id(user_id)

    def update_review(self, review_id: str, review_data: Dict[str, Any]) -> bool:
        """Update review with validation"""
        try:
            review = self.get_review(review_id)
            if not review:
                return False
            
            # Validate place and user exist if being updated
            if 'place_id' in review_data and not self.place_repo.exists(review_data['place_id']):
                raise ValueError("Place does not exist")
            
            if 'user_id' in review_data and not self.user_repo.exists(review_data['user_id']):
                raise ValueError("User does not exist")
            
            return self.review_repo.update(review_id, review_data)
        except Exception as e:
            print(f"Error updating review: {e}")
            return False

    def delete_review(self, review_id: str) -> bool:
        """Delete review"""
        return self.review_repo.delete(review_id)

    # ========== AMENITY OPERATIONS ==========
    
    def create_amenity(self, amenity_data: Dict[str, Any]) -> Optional[Amenity]:
        """Create a new amenity with validation"""
        try:
            # Validate required fields
            if 'name' not in amenity_data or not amenity_data['name']:
                raise ValueError("Amenity name is required")
            
            # Check if amenity already exists
            if self.amenity_repo.get_by_name(amenity_data['name']):
                raise ValueError("Amenity already exists")
            
            # Create amenity
            amenity = Amenity(**amenity_data)
            if self.amenity_repo.add(amenity):
                return amenity
            return None
        except Exception as e:
            print(f"Error creating amenity: {e}")
            return None

    def get_amenity(self, amenity_id: str) -> Optional[Amenity]:
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self) -> List[Amenity]:
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def search_amenities(self, name: str) -> List[Amenity]:
        """Search amenities by name"""
        return self.amenity_repo.search_by_name(name)

    def update_amenity(self, amenity_id: str, amenity_data: Dict[str, Any]) -> bool:
        """Update amenity with validation"""
        try:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                return False
            
            # Check if new name already exists
            if 'name' in amenity_data and amenity_data['name'] != amenity.name:
                existing_amenity = self.amenity_repo.get_by_name(amenity_data['name'])
                if existing_amenity:
                    raise ValueError("Amenity name already exists")
            
            return self.amenity_repo.update(amenity_id, amenity_data)
        except Exception as e:
            print(f"Error updating amenity: {e}")
            return False

    def delete_amenity(self, amenity_id: str) -> bool:
        """Delete amenity and remove from all places"""
        try:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                return False
            
            # Remove amenity from all places
            all_places = self.place_repo.get_all()
            for place in all_places:
                if amenity_id in place.amenity_ids:
                    place.remove_amenity(amenity_id)
            
            return self.amenity_repo.delete(amenity_id)
        except Exception as e:
            print(f"Error deleting amenity: {e}")
            return False

    # ========== UTILITY METHODS ==========
    
    def get_statistics(self) -> Dict[str, int]:
        """Get basic statistics about the system"""
        return {
            'total_users': self.user_repo.count(),
            'total_places': self.place_repo.count(),
            'total_reviews': self.review_repo.count(),
            'total_amenities': self.amenity_repo.count()
        }

    def clear_all_data(self):
        """Clear all data from all repositories (useful for testing)"""
        self.user_repo.clear()
        self.place_repo.clear()
        self.review_repo.clear()
        self.amenity_repo.clear() 