"""
Composition is one of the fundamental principles of object-oriented programming (OOP). 
It allows objects to be built using other objects, promoting code reuse, flexibility, and better maintainability. 
Unlike inheritance, which establishes an "is-a" relationship, composition represents a "has-a" relationship.

Composition is a design principle in OOP where one class contains an instance (or instances) of another class as a field. 
The contained class is often called a component, and the containing class is referred to as a composite class. 
This helps in building complex systems by combining simpler objects.

When to Use Composition?
- When building complex objects that consist of multiple components.
- When you want to achieve code reusability without rigid inheritance hierarchies.
- When different behaviors need to be swapped dynamically (e.g., using different types of engines in a vehicle).
- When following the favor composition over inheritance principle.
"""

# Consider a Car that consists of multiple components like an Engine, Wheel, and Transmission. 
# Instead of inheriting from these components, a Car object will contain them as fields.

class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower
    
    def start(self):
        print(f"Engine started with {self.horsepower} HP.")


class Wheel:
    def __init__(self, type):
        self.type = type
    
    def rotate(self):
        print(f"The {self.type} wheel is rotating.")


class Transmission:
    def __init__(self, type):
        self.type = type
    
    def shift_gear(self):
        print(f"Transmission shifted: {self.type}")


class Car:
    def __init__(self, engine, wheel, transmission):
        self.engine = engine
        self.wheel = wheel
        self.transmission = transmission
    
    def drive(self):
        self.engine.start()
        self.wheel.rotate()
        self.transmission.shift_gear()
        print("Car is moving!")


# Example Usage
if __name__ == "__main__":
    engine = Engine(150)
    wheel = Wheel("Alloy")
    transmission = Transmission("Automatic")
    
    car = Car(engine, wheel, transmission)
    car.drive()