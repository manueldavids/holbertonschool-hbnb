from app.models import BaseModel

class Place(BaseModel):
    def __init__(self, **kwargs):
        # Place-specific attributes
        self.city_id = kwargs.get('city_id', '')
        self.user_id = kwargs.get('user_id', '')
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.number_rooms = kwargs.get('number_rooms', 0)
        self.number_bathrooms = kwargs.get('number_bathrooms', 0)
        self.max_guest = kwargs.get('max_guest', 0)
        self.price_by_night = kwargs.get('price_by_night', 0)
        self.latitude = kwargs.get('latitude', 0.0)
        self.longitude = kwargs.get('longitude', 0.0)
        self.amenity_ids = kwargs.get('amenity_ids', [])
        
        # Call parent constructor
        super().__init__(**kwargs)
    
    def add_amenity(self, amenity_id):
        """Add an amenity to the place"""
        if amenity_id not in self.amenity_ids:
            self.amenity_ids.append(amenity_id)
    
    def remove_amenity(self, amenity_id):
        """Remove an amenity from the place"""
        if amenity_id in self.amenity_ids:
            self.amenity_ids.remove(amenity_id)
    
    def __str__(self):
        """String representation of Place"""
        return f"[Place] ({self.id}) {self.name}"