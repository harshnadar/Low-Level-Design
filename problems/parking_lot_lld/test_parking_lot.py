from parking_lot import ParkingLot, Level, ParkingSpot, Vehicle
from entry import Entry
from exit import Exit
from vehicle_types import VehicleType

def test():
    # Initialize system
    parking_lot = ParkingLot()

    # Create levels and spots
    level1 = Level("L1")
    for i in range(10):
        level1.add_spot(ParkingSpot(f"L1-M{i}", VehicleType.MOTORCYCLE))
    for i in range(5):
        level1.add_spot(ParkingSpot(f"L1-T{i}", VehicleType.TRUCK))
    for i in range(7):
        level1.add_spot(ParkingSpot(f"L1-C{i}", VehicleType.CAR))
    parking_lot.add_level(level1)

    # Create entry/exit points
    entry1 = Entry("E1", parking_lot)
    exit1 = Exit("X1", parking_lot)

    # Vehicle entry
    car = Vehicle("ABC123", VehicleType.CAR)
    print(entry1.process_entry(car))  # Parks in truck spot if car spots full

    # Vehicle exit
    spot = parking_lot.park_vehicle(car)  # Get spot reference
    print(exit1.process_exit(spot))

import threading
import time
import random
from parking_lot import ParkingLot, Level, ParkingSpot, Vehicle
from entry import Entry
from exit import Exit
from vehicle_types import VehicleType
from typing import List
import unittest

class TestParkingLotConcurrency(unittest.TestCase):
    def setUp(self):
        self.parking_lot = ParkingLot()
        self.level1 = Level("L1")
        
        # Add spots
        for i in range(5):
            self.level1.add_spot(ParkingSpot(f"L1-M{i}", VehicleType.MOTORCYCLE))
            self.level1.add_spot(ParkingSpot(f"L1-C{i}", VehicleType.CAR))
            self.level1.add_spot(ParkingSpot(f"L1-T{i}", VehicleType.TRUCK))
        
        self.parking_lot.add_level(self.level1)
        self.entry = Entry("E1", self.parking_lot)
        self.exit = Exit("X1", self.parking_lot)
        
        # Track parked vehicles and their spots
        self.parked_vehicles: List[tuple] = []
        self.park_lock = threading.Lock()

    def test_concurrent_parking(self):
        """Test multiple vehicles trying to park and exit simultaneously"""
        num_vehicles = 20
        threads = []
        results = []
        
        def park_and_exit():
            # Create a vehicle with random type
            vehicle_type = random.choice([VehicleType.MOTORCYCLE, VehicleType.CAR, VehicleType.TRUCK])
            vehicle = Vehicle(f"VEH-{threading.get_ident()}", vehicle_type)
            
            # Try to park
            spot = self.parking_lot.park_vehicle(vehicle)
            if spot:
                with self.park_lock:
                    self.parked_vehicles.append((vehicle, spot))
                    results.append(True)
                
                # Simulate some parking duration
                time.sleep(random.uniform(0.1, 0.5))
                
                # Exit the vehicle
                self.exit.process_exit(spot)
            else:
                results.append(False)

        # Create and start threads
        start_time = time.time()
        for _ in range(num_vehicles):
            thread = threading.Thread(target=park_and_exit)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        end_time = time.time()

        # Assertions and verifications
        print(f"\nConcurrency Test Results:")
        print(f"Total vehicles processed: {num_vehicles}")
        print(f"Successfully parked vehicles: {sum(results)}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        
        # Verify no spots are occupied after all operations
        for spot_type in self.level1.spots.values():
            for spot in spot_type:
                self.assertFalse(spot.is_occupied(), "All spots should be free after test")

    def test_concurrent_same_spot(self):
        """Test multiple threads trying to park in the same spot"""
        num_threads = 10
        successful_parks = []
        
        def try_park_same_spot():
            vehicle = Vehicle(f"VEH-{threading.get_ident()}", VehicleType.CAR)
            if spot := self.parking_lot.park_vehicle(vehicle):
                successful_parks.append((vehicle, spot))
                time.sleep(0.1)  # Hold the spot briefly
                self.exit.process_exit(spot)

        # Get the first available car spot
        first_car = Vehicle("FIRST-CAR", VehicleType.CAR)
        first_spot = self.parking_lot.park_vehicle(first_car)
        self.exit.process_exit(first_spot)  # Free it up for the test

        # Launch concurrent threads
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=try_park_same_spot)
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join()

        # Verify that spots were never double-booked
        spot_usage = {}
        for vehicle, spot in successful_parks:
            if spot.spot_id in spot_usage:
                self.fail(f"Spot {spot.spot_id} was double-booked!")
            spot_usage[spot.spot_id] = vehicle

        print(f"\nConcurrent Same Spot Test Results:")
        print(f"Total attempts: {num_threads}")
        print(f"Successful parks: {len(successful_parks)}")

def run_concurrency_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParkingLotConcurrency)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    run_concurrency_tests()

# if __name__ == "__main__":
#     test()
