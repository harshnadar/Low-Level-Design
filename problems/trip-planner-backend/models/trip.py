from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

@dataclass
class Trip:
    id: str
    name: str
    destination: str
    start_date: str
    end_date: str
    description: Optional[str] = ""
    budget: Optional[float] = 0.0
    
    def __post_init__(self):
        # Validate required fields
        if not self.name or not self.destination:
            raise ValueError("Name and destination are required")
        
        # Validate dates
        try:
            start = datetime.fromisoformat(self.start_date)
            end = datetime.fromisoformat(self.end_date)
            if end < start:
                raise ValueError("End date must be after start date")
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")
        
        # Ensure budget is non-negative
        if self.budget is not None and self.budget < 0:
            raise ValueError("Budget cannot be negative")
    
    def to_dict(self):
        return asdict(self)