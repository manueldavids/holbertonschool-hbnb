from .base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"Amenity(id={self.id}, name={self.name})"