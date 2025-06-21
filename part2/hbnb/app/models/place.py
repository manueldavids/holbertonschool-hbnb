from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price  # This will use the property setter
        self.latitude = latitude  # This will use the property setter
        self.longitude = longitude  # This will use the property setter
        self.owner_id = owner_id
        self.amenities = amenities or []

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        """Validate price is non-negative float"""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Validate latitude is between -90 and 90"""
        if not isinstance(value, (int, float)) or not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Validate longitude is between -180 and 180"""
        if not isinstance(value, (int, float)) or not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)

    def add_amenity(self, amenity_id):
        """Add an amenity to the place"""
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)

    def remove_amenity(self, amenity_id):
        """Remove an amenity from the place"""
        if amenity_id in self.amenities:
            self.amenities.remove(amenity_id)

    def __str__(self):
        return f"Place(id={self.id}, title={self.title}, price={self.price}, owner_id={self.owner_id})"