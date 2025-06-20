from app.models import BaseModel

class Amenity(BaseModel):
    def __init__(self, **kwargs):
        # Amenity-specific attributes
        self.name = kwargs.get('name', '')
        
        # Call parent constructor
        super().__init__(**kwargs)
    
    def __str__(self):
        """String representation of Amenity"""
        return f"[Amenity] ({self.id}) {self.name}"