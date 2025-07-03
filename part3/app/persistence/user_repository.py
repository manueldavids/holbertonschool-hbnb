"""
User repository for database operations specific to User entity.
Extends the generic SQLAlchemyRepository with user-specific functionality.
"""

from typing import List, Optional, Dict, Any
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """
    User-specific repository for database operations.
    Extends SQLAlchemyRepository with user-specific queries and operations.
    """
    
    def __init__(self):
        """
        Initialize UserRepository with User model.
        """
        super().__init__(User)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.
        
        Args:
            email (str): User email address
            
        Returns:
            User: User instance if found, None otherwise
        """
        if not email:
            return None
        
        return self.model.query.filter_by(
            email=email.lower().strip()
        ).first()
    
    def get_users_by_admin_status(self, is_admin: bool) -> List[User]:
        """
        Get users by admin status.
        
        Args:
            is_admin (bool): Admin status to filter by
            
        Returns:
            list: List of User instances with specified admin status
        """
        return self.model.query.filter_by(is_admin=is_admin).all()
    
    def get_users_by_name(self, first_name: str = None, 
                         last_name: str = None) -> List[User]:
        """
        Get users by name (first name and/or last name).
        
        Args:
            first_name (str, optional): First name to filter by
            last_name (str, optional): Last name to filter by
            
        Returns:
            list: List of User instances matching the name criteria
        """
        query = self.model.query
        
        if first_name:
            query = query.filter(
                self.model.first_name.ilike(f'%{first_name}%')
            )
        
        if last_name:
            query = query.filter(
                self.model.last_name.ilike(f'%{last_name}%')
            )
        
        return query.all()
    
    def create_user(self, user_data: Dict[str, Any]) -> Optional[User]:
        """
        Create a new user with password hashing.
        
        Args:
            user_data (dict): User data containing email, password, etc.
            
        Returns:
            User: Created user instance or None if failed
        """
        try:
            # Create user instance with password hashing
            user = User(
                email=user_data.get('email'),
                password=user_data.get('password'),
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
                is_admin=user_data.get('is_admin', False)
            )
            
            # Save to database
            self.add(user)
            
            return user
            
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def update_user_password(self, user_id: str, new_password: str) -> bool:
        """
        Update user password.
        
        Args:
            user_id (str): User ID to update
            new_password (str): New password
            
        Returns:
            bool: True if update was successful
        """
        try:
            user = self.get(user_id)
            if user:
                user.update_password(new_password)
                self.model.query.session.commit()
                return True
            return False
            
        except Exception as e:
            print(f"Error updating user password: {e}")
            return False
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password.
        
        Args:
            email (str): User email
            password (str): User password
            
        Returns:
            User: User instance if authentication successful, None otherwise
        """
        user = self.get_user_by_email(email)
        if user and user.verify_password(password):
            return user
        return None
    
    def get_user_count_by_admin_status(self, is_admin: bool) -> int:
        """
        Get count of users by admin status.
        
        Args:
            is_admin (bool): Admin status to count
            
        Returns:
            int: Number of users with specified admin status
        """
        return self.model.query.filter_by(is_admin=is_admin).count()
    
    def search_users(self, search_term: str) -> List[User]:
        """
        Search users by email, first name, or last name.
        
        Args:
            search_term (str): Term to search for
            
        Returns:
            list: List of User instances matching the search term
        """
        if not search_term:
            return []
        
        search_pattern = f'%{search_term}%'
        
        return self.model.query.filter(
            (self.model.email.ilike(search_pattern)) |
            (self.model.first_name.ilike(search_pattern)) |
            (self.model.last_name.ilike(search_pattern))
        ).all() 