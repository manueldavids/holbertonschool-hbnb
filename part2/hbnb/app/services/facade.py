from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Create a user
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    
    # Get a user by ID
    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    # Update a user
    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if user:
            user.update(user_data)
            return user
        return None

    # Get a user by email
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # Get all users
    def get_all_users(self):
        return self.user_repo.get_all()

    # Create an amenity
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    # Get an amenity by ID
    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    # Get all amenities
    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    # Update an amenity
    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
            return amenity
        return None

    def create_place(self, place_data):
        """Create a new place with validation"""
        # Validate owner exists
        owner = self.get_user(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")
        
        # Validate amenities exist (si se proporcionan)
        amenity_ids = place_data.get('amenities', [])
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with ID {amenity_id} not found")
        
        # Create place (las validaciones de price, lat, long se hacen en el modelo)
        try:
            place = Place(**place_data)
            self.place_repo.add(place)
            return place
        except ValueError as e:
            raise ValueError(f"Invalid place data: {str(e)}")

    def get_place(self, place_id):
        """Get a place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place"""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        # Validate owner if being updated
        if 'owner_id' in place_data:
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
        
        # Validate amenities if being updated
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} not found")
        
        try:
            place.update(place_data)
            return place
        except ValueError as e:
            raise ValueError(f"Invalid update data: {str(e)}")