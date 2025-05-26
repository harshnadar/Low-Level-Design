from typing import Dict, List, Optional, Generic, TypeVar
from src.exceptions.custom_exceptions import ResourceNotFoundException

T = TypeVar('T')


class InMemoryRepository(Generic[T]):
    """Generic in-memory repository for storing entities"""
    
    def __init__(self):
        self._storage: Dict[str, T] = {}

    def save(self, entity_id: str, entity: T) -> T:
        """Save an entity"""
        self._storage[entity_id] = entity
        return entity

    def find_by_id(self, entity_id: str) -> Optional[T]:
        """Find an entity by ID"""
        return self._storage.get(entity_id)

    def find_all(self) -> List[T]:
        """Get all entities"""
        return list(self._storage.values())

    def delete(self, entity_id: str) -> bool:
        """Delete an entity"""
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False

    def exists(self, entity_id: str) -> bool:
        """Check if an entity exists"""
        return entity_id in self._storage

    def clear(self):
        """Clear all entities"""
        self._storage.clear()

    def update(self, entity_id: str, entity: T) -> T:
        """Update an existing entity"""
        if entity_id not in self._storage:
            raise ResourceNotFoundException(f"Entity with ID {entity_id} not found")
        self._storage[entity_id] = entity
        return entity