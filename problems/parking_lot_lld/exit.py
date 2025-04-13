from parking_lot import ParkingLot
from parking_spot import ParkingSpot

class Exit:
    def __init__(self, entry_id: str, parking_lot: ParkingLot):
        self.parking_lot = parking_lot
        self.entry_id = entry_id

    def process_exit(self, spot: ParkingSpot):
        self.parking_lot.exit_vehicle(spot)
        print(f"Vehicle exited from spot {spot.spot_id}.")
