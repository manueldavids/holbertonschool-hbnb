from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class Repository(ABC):
    @abstractmethod
    def add(self, obj) -> bool:
        """Add an object to the repository"""
        pass

    @abstractmethod
    def get(self, obj_id: str):
        """Get an object by ID"""
        pass

    @abstractmethod
    def get_all(self) -> List:
        """Get all objects"""
        pass

    @abstractmethod
    def update(self, obj_id: str, data: Dict[str, Any]) -> bool:
        """Update an object by ID with new data"""
        pass

    @abstractmethod
    def delete(self, obj_id: str) -> bool:
        """Delete an object by ID"""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name: str, attr_value: Any):
        """Get object by specific attribute value"""
        pass

    @abstractmethod
    def get_by_attributes(self, attributes: Dict[str, Any]) -> List:
        """Get objects matching multiple attributes"""
        pass

    @abstractmethod
    def exists(self, obj_id: str) -> bool:
        """Check if object exists by ID"""
        pass

    @abstractmethod
    def count(self) -> int:
        """Get total count of objects"""
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}
        self._counter = 0

    def add(self, obj) -> bool:
        """Add an object to the repository"""
        try:
            if not hasattr(obj, 'id'):
                raise ValueError("Object must have an 'id' attribute")
            
            if obj.id in self._storage:
                return False  # Object already exists
            
            self._storage[obj.id] = obj
            self._counter += 1
            return True
        except Exception as e:
            print(f"Error adding object: {e}")
            return False

    def get(self, obj_id: str):
        """Get an object by ID"""
        return self._storage.get(obj_id)

    def get_all(self) -> List:
        """Get all objects"""
        return list(self._storage.values())

    def update(self, obj_id: str, data: Dict[str, Any]) -> bool:
        """Update an object by ID with new data"""
        try:
            obj = self.get(obj_id)
            if obj:
                obj.update(data)
                return True
            return False
        except Exception as e:
            print(f"Error updating object: {e}")
            return False

    def delete(self, obj_id: str) -> bool:
        """Delete an object by ID"""
        if obj_id in self._storage:
            del self._storage[obj_id]
            self._counter -= 1
            return True
        return False

    def get_by_attribute(self, attr_name: str, attr_value: Any):
        """Get object by specific attribute value"""
        for obj in self._storage.values():
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
                return obj
        return None

    def get_by_attributes(self, attributes: Dict[str, Any]) -> List:
        """Get objects matching multiple attributes"""
        matching_objects = []
        for obj in self._storage.values():
            matches = True
            for attr_name, attr_value in attributes.items():
                if not hasattr(obj, attr_name) or getattr(obj, attr_name) != attr_value:
                    matches = False
                    break
            if matches:
                matching_objects.append(obj)
        return matching_objects

    def exists(self, obj_id: str) -> bool:
        """Check if object exists by ID"""
        return obj_id in self._storage

    def count(self) -> int:
        """Get total count of objects"""
        return len(self._storage)

    def clear(self):
        """Clear all objects from repository (useful for testing)"""
        self._storage.clear()
        self._counter = 0

    def get_ids(self) -> List[str]:
        """Get list of all object IDs"""
        return list(self._storage.keys())