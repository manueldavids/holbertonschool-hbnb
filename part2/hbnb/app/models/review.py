from .base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.place_id = place_id
        self.user_id = user_id

    def _validate_text(self, text):
        """Validate that review text is not empty"""
        if not text or not text.strip():
            raise ValueError("Review text cannot be empty")
        if not isinstance(text, str):
            raise ValueError("Review text must be a string")
        if len(text.strip()) < 1:
            raise ValueError("Review text cannot be empty")
        return text.strip()

    def _validate_rating(self, rating):
        """Validate rating is between 1 and 5"""
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating

    def __str__(self):
        return f"Review(id={self.id}, place_id={self.place_id}, user_id={self.user_id}, rating={self.rating})"