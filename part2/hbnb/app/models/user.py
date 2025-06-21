import re
from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = self._validate_name(first_name, "First name")
        self.last_name = self._validate_name(last_name, "Last name")
        self.email = self._validate_email(email)
        self.is_admin = is_admin

    def _validate_name(self, name, field_name):
        """Validate that name is not empty and contains only letters and spaces"""
        if not name or not name.strip():
            raise ValueError(f"{field_name} cannot be empty")
        if not isinstance(name, str):
            raise ValueError(f"{field_name} must be a string")
        if len(name.strip()) < 1:
            raise ValueError(f"{field_name} cannot be empty")
        return name.strip()

    def _validate_email(self, email):
        """Validate email format"""
        if not email or not email.strip():
            raise ValueError("Email cannot be empty")
        
        # Basic email regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email.strip()):
            raise ValueError("Invalid email format")
        
        return email.strip().lower()

    def __str__(self):
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, is_admin={self.is_admin})"