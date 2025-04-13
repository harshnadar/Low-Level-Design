from parking_lot import ParkingLot
from vehicle import Vehicle
class Entry:
    def __init__(self, entry_id: str, parking_lot: ParkingLot):
        self.entry_id = entry_id
        self.parking_lot = parking_lot

    def process_entry(self, vehicle: Vehicle):
        if spot := self.parking_lot.park_vehicle(vehicle):
            print(f"Vehicle {vehicle.get_license_plate()} parked at spot {spot.spot_id}.")
        else:
            print(f"Failed to park vehicle {vehicle.get_license_plate()}.")

