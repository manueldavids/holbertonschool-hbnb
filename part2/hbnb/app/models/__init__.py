import uuid
from datetime import datetime

class BaseModel:
    def __init__(self, **kwargs):
        # Generate unique ID if not provided
        self.id = kwargs.get('id', str(uuid.uuid4()))
        
        # Set creation and update timestamps
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())
        
        # Set other attributes from kwargs
        for key, value in kwargs.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
    
    def update(self, data):
        """Update model attributes with new data"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert model to dictionary representation"""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result
    
    def __str__(self):
        """String representation of the model"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"