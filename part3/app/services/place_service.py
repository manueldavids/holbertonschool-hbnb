"""
Place service layer for business logic operations.
Separates business logic from API endpoints.
"""

from typing import List, Optional, Dict, Any
from app.models.place import Place
from app.models.user import User
from app import db
import uuid


class PlaceService:
    """
    Service class for place-related business operations.
    """

    @staticmethod
    def create_place(place_data: Dict[str, Any],
                     owner_id: str) -> Optional[Place]:
        """
        Create a new place.

        Args:
            place_data (dict): Place data from request
            owner_id (str): ID of the place owner

        Returns:
            Place: Created place instance or None if failed
        """
        try:
            # Validate required fields
            if not place_data.get('name'):
                return None

            # Create new place
            place = Place(
                name=place_data.get('name'),
                description=place_data.get('description'),
                address=place_data.get('address'),
                price_per_night=place_data.get('price_per_night'),
                max_guests=place_data.get('max_guests'),
                latitude=place_data.get('latitude'),
                longitude=place_data.get('longitude'),
                owner_id=owner_id
            )

            # Save to database
            db.session.add(place)
            db.session.commit()

            return place

        except Exception as e:
            db.session.rollback()
            print(f"Error creating place: {str(e)}")
            return None

    @staticmethod
    def get_place_by_id(place_id: str) -> Optional[Place]:
        """
        Get place by ID.

        Args:
            place_id (str): Place ID to search for

        Returns:
            Place: Place instance or None if not found
        """
        try:
            return Place.get_by_id(place_id)
        except Exception as e:
            print(f"Error getting place by ID: {str(e)}")
            return None

    @staticmethod
    def get_all_places() -> List[Place]:
        """
        Get all places.

        Returns:
            list: List of all Place instances
        """
        try:
            return Place.get_all()
        except Exception as e:
            print(f"Error getting all places: {str(e)}")
            return []

    @staticmethod
    def update_place(place_id: str, update_data: Dict[str, Any],
                     user_id: str) -> Optional[Place]:
        """
        Update place if user is the owner.

        Args:
            place_id (str): Place ID to update
            update_data (dict): Data to update
            user_id (str): ID of the user making the request

        Returns:
            Place: Updated place instance or None if failed
        """
        try:
            # Get place
            place = Place.get_by_id(place_id)
            if not place:
                return None

            # Check ownership
            if str(place.owner_id) != user_id:
                return None

            # Update place
            if place.update_from_dict(update_data):
                db.session.commit()
                return place

            return None

        except Exception as e:
            db.session.rollback()
            print(f"Error updating place: {str(e)}")
            return None

    @staticmethod
    def delete_place(place_id: str, user_id: str) -> bool:
        """
        Delete place if user is the owner.

        Args:
            place_id (str): Place ID to delete
            user_id (str): ID of the user making the request

        Returns:
            bool: True if deletion was successful
        """
        try:
            # Get place
            place = Place.get_by_id(place_id)
            if not place:
                return False

            # Check ownership
            if str(place.owner_id) != user_id:
                return False

            # Delete place
            db.session.delete(place)
            db.session.commit()

            return True

        except Exception as e:
            db.session.rollback()
            print(f"Error deleting place: {str(e)}")
            return False

    @staticmethod
    def get_places_by_owner(owner_id: str) -> List[Place]:
        """
        Get all places owned by a specific user.

        Args:
            owner_id (str): Owner user ID

        Returns:
            list: List of Place instances owned by the user
        """
        try:
            return Place.get_by_owner(owner_id)
        except Exception as e:
            print(f"Error getting places by owner: {str(e)}")
            return []

    @staticmethod
    def validate_place_data(place_data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate place data.

        Args:
            place_data (dict): Place data to validate

        Returns:
            tuple: (is_valid, error_message)
        """
        # Check required fields
        if not place_data.get('name'):
            return False, "Place name is required"

        # Validate price_per_night
        if 'price_per_night' in place_data:
            try:
                price = float(place_data['price_per_night'])
                if price < 0:
                    return False, "Price per night cannot be negative"
            except (ValueError, TypeError):
                return False, "Invalid price per night value"

        # Validate max_guests
        if 'max_guests' in place_data:
            try:
                guests = int(place_data['max_guests'])
                if guests <= 0:
                    return False, "Maximum guests must be positive"
            except (ValueError, TypeError):
                return False, "Invalid maximum guests value"

        # Validate coordinates
        if 'latitude' in place_data:
            try:
                lat = float(place_data['latitude'])
                if not -90 <= lat <= 90:
                    return False, "Latitude must be between -90 and 90"
            except (ValueError, TypeError):
                return False, "Invalid latitude value"

        if 'longitude' in place_data:
            try:
                lon = float(place_data['longitude'])
                if not -180 <= lon <= 180:
                    return False, "Longitude must be between -180 and 180"
            except (ValueError, TypeError):
                return False, "Invalid longitude value"

        return True, ""
