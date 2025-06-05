from typing import List, Dict, Any
from .base_repository import BaseRepository
from config import Config

class ItineraryRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.ITINERARIES_FILE)
    
    def get_by_trip_id(self, trip_id: str) -> List[Dict[str, Any]]:
        """Get all itineraries for a specific trip"""
        all_itineraries = self.get_all()
        return [itinerary for itinerary in all_itineraries 
                if itinerary.get('trip_id') == trip_id]