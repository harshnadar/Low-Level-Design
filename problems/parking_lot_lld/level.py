from collections import defaultdict, deque
from threading import RLock
from vehicle_types import VehicleType
from parking_spot import ParkingSpot
from typing import Optional

class Level:
    def __init__(self, level_id: str):
        self.level_id = level_id
        self.spots = defaultdict(deque)
        self._lock = RLock()

    def add_spot(self, spot: ParkingSpot) -> None:
        with self._lock:
            self.spots[spot.spot_type].append(spot)

    def find_available_spot(self, vehicle_type: VehicleType) -> Optional[ParkingSpot]:
        """
        Find an available parking spot for the given vehicle type.
        Can assign larger spots if exact size is unavailable.
        """
        with self._lock:
            # Convert enum to int for comparison
            required_size = vehicle_type.value
            # Sort spot types by size (smallest to largest)
            compatible_spots = [
                spot_type for spot_type in VehicleType 
                if isinstance(spot_type, VehicleType) and spot_type.value >= required_size
            ]
            
            for spot_type in sorted(compatible_spots, key=lambda x: x.value):
                if self.spots[spot_type] and len(self.spots[spot_type]) > 0:
                    return self.spots[spot_type].popleft()
            return None
        
    def free_spot(self, spot: ParkingSpot) -> None:
        """Return a spot back to the available spots pool"""
        with self._lock:
            self.spots[spot.spot_type].append(spot)