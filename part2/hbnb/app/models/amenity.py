from .base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = self._validate_name(name)

    def _validate_name(self, name):
        """Validate that amenity name is not empty"""
        if not name or not name.strip():
            raise ValueError("Amenity name cannot be empty")
        if not isinstance(name, str):
            raise ValueError("Amenity name must be a string")
        if len(name.strip()) < 1:
            raise ValueError("Amenity name cannot be empty")
        return name.strip()

    def __str__(self):
        return f"Amenity(id={self.id}, name={self.name})"