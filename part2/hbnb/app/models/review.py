from app.models import BaseModel

class Review(BaseModel):
    def __init__(self, **kwargs):
        # Review-specific attributes
        self.place_id = kwargs.get('place_id', '')
        self.user_id = kwargs.get('user_id', '')
        self.text = kwargs.get('text', '')
        
        # Call parent constructor
        super().__init__(**kwargs)
    
    def __str__(self):
        """String representation of Review"""
        return f"[Review] ({self.id}) {self.text[:50]}..."