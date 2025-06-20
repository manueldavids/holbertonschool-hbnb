from app.models import BaseModel

class User(BaseModel):
    def __init__(self, **kwargs):
        # User-specific attributes
        self.email = kwargs.get('email', '')
        self.password = kwargs.get('password', '')
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
        
        # Call parent constructor
        super().__init__(**kwargs)
    
    def to_dict(self):
        """Convert user to dictionary, excluding password for security"""
        user_dict = super().to_dict()
        # Remove password from dictionary representation
        user_dict.pop('password', None)
        return user_dict
    
    def __str__(self):
        """String representation of User"""
        return f"[User] ({self.id}) {self.email}"