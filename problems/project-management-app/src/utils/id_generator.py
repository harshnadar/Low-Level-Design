import uuid
from typing import Dict


class IdGenerator:
    """Singleton class for generating unique IDs"""
    _instance = None
    _counters: Dict[str, int] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IdGenerator, cls).__new__(cls)
        return cls._instance

    @classmethod
    def generate_id(cls, prefix: str) -> str:
        """Generate a unique ID with a given prefix"""
        if prefix not in cls._counters:
            cls._counters[prefix] = 0
        cls._counters[prefix] += 1
        return f"{prefix}_{cls._counters[prefix]}"

    @classmethod
    def generate_uuid(cls) -> str:
        """Generate a UUID-based ID"""
        return str(uuid.uuid4())

    @classmethod
    def reset(cls):
        """Reset counters - useful for testing"""
        cls._counters.clear()