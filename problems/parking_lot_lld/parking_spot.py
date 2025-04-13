from vehicle_types import VehicleType
from vehicle import Vehicle
from threading import Lock

class ParkingSpot:
    def __init__(self, spot_id: str, vehicle_type: VehicleType = VehicleType.CAR):
        """
        Initialize a parking spot.
        :param spot_number: The number of the parking spot.
        :param vehicle_type: The type of vehicle that can be parked in this spot. Car by default.
        :param parked_vehicle: The vehicle currently parked in this spot (if any).
        """
        self.spot_id = spot_id
        self.parked_vehicle: Vehicle = None
        self.spot_type = vehicle_type
        self._lock = Lock()

    def is_available(self) -> bool:
        """
        Check if the parking spot is available.
        :return: True if the spot is available, False otherwise.
        """
        return self.parked_vehicle is None
    
    def park_vehicle(self, vehicle: Vehicle) -> bool:
        """
        Park a vehicle in the parking spot.
        :param vehicle: The vehicle to park.
        :return: True if the vehicle was parked successfully, False otherwise.
        """
        with self._lock:
            if self.is_available():
                self.parked_vehicle = vehicle
                return True
            return False
    
    def unpark_vehicle(self) -> bool:
        with self._lock:
            self.parked_vehicle = None

