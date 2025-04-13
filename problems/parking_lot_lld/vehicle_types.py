from enum import Enum

class VehicleType(Enum):
    """
    Enum representing different types of vehicles.
    """
    CAR = 1
    MOTORCYCLE = 2
    TRUCK = 3

    # This method returns the string representation of the vehicle type.
    # def __str__(self):
    #     return self.name.capitalize()
    
    