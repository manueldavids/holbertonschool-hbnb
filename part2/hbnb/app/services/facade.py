from app.persistence.repository import InMemoryRepository
from app.models.user import User

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
        # Placeholder for logic to create an amenity
        pass

    # Get an amenity by ID
    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        pass

    # Get all amenities
    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        pass

    # Update an amenity
    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        pass