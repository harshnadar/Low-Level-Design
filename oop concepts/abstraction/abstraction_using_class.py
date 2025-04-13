
"""
Python provides the ABC module to define abstract classes.
Why Use Abstract Classes?

- Allows defining common behavior that subclasses must implement.
- Enables partial abstraction (can have both abstract and concrete methods).
- Prevents direct instantiation of base classes.
"""
from abc import ABC, abstractmethod

# Abstract class
class Vehicle(ABC):
    def __init__(self, brand):
        self.brand = brand
    
    @abstractmethod
    def start(self):
        pass  # Abstract method (must be implemented by subclasses)
    
    def display_brand(self):
        print(f"Brand: {self.brand}")

# Subclass implementing the abstract method
class Car(Vehicle):
    def start(self):
        print("Car is starting...")

if __name__ == "__main__":
    car = Car("Toyota")
    car.display_brand()
    car.start()