from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class Itinerary:
    id: str
    trip_id: str
    day: int
    activities: List[str]
    notes: Optional[str] = ""
    
    def __post_init__(self):
        # Validate required fields
        if not self.trip_id:
            raise ValueError("Trip ID is required")
        
        # Validate day
        if self.day < 1:
            raise ValueError("Day must be a positive integer")
        
        # Ensure activities is a list
        if not isinstance(self.activities, list):
            raise ValueError("Activities must be a list")
    
    def to_dict(self):
        return asdict(self)