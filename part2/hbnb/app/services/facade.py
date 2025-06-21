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

    # Get a user by email
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        pass

    # Get all places
    def get_all_places(self, place_id):
        pass

    # Update a place
    def update_place(self, place_id, place_data):
        pass
    
    # Delete a place
    def delete_place(self, place_id):
        pass

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

    # Create a place
    def create_place(self, place_data):
        # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        pass

    # Get a place by ID
    def get_place(self, place_id):
    # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        pass

    # Get all places
    def get_all_places(self):
    # Placeholder for logic to retrieve all places
        pass

    # Update a place
    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        pass

    # Create a review
    def create_review(self, review_data):
        # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        pass

    # Get a review by ID
    def get_review(self, review_id):
    # Placeholder for logic to retrieve a review by ID
        pass

    # Get all reviews
    def get_all_reviews(self):
    # Placeholder for logic to retrieve all reviews
        pass

    # Get reviews by place
    def get_reviews_by_place(self, place_id):
    # Placeholder for logic to retrieve all reviews for a specific place
        pass

    # Update a review
    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        pass

    # Delete a review
    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        pass