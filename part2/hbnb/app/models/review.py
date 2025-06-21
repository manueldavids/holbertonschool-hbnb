from .base_model import BaseModel


class Review(BaseModel):
    def __init__(self, place, user, rating, text):
        super().__init__()
        self.place = Place(place)
        self.user = User(user)
        self.rating = rating
        self.text = text

    def __str__(self):
        return f"Review(id={self.id}, place={self.place}, user={self.user}, rating={self.rating}, text={self.text})"