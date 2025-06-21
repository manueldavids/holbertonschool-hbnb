from models.base_model import BaseModel
from models.place import Place
from models.user import User

class Review(BaseModel):
    def __init__(self, place, user, rating, text):
        super().__init__()
        self.place = Place(place)
        self.user = User(user)
        self.rating = rating
        self.text = text