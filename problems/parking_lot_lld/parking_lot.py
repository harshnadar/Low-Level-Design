import threading
from level import Level
from vehicle import Vehicle
from parking_spot import ParkingSpot
from typing import Optional, List


class ParkingLot:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.levels: List[Level]= []
                cls._instance.entry_lock = threading.Lock()

            return cls._instance
        
    def add_level(self, level: Level) -> None:
        self.levels.append(level)
        print("Added level:", level.level_id)

    def park_vehicle(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        for level in self.levels:
            if spot := level.find_available_spot(vehicle.vehicle_type):
                if spot.park_vehicle(vehicle):
                    return spot
        return None
    
    def exit_vehicle(self, spot: ParkingSpot) -> None:
        for level in self.levels:
            if spot in level.spots[spot.spot_type]:
                if spot.unpark_vehicle():
                    level.free_spot(spot)
                    return

