from abc import ABC, abstractmethod
from vehicle_types import VehicleType

class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.vehicle_type = vehicle_type
        self._license_plate = license_plate

    def get_type(self) -> VehicleType:
        return self.vehicle_type
    
    def get_license_plate(self) -> str:
        return self._license_plate
