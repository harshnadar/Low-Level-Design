from abc import ABC, abstractmethod

class Engine(ABC):
    @abstractmethod
    def start(self):
        pass


class PetrolEngine(Engine):
    def start(self):
        print("Petrol Engine started.")


class DieselEngine(Engine):
    def start(self):
        print("Diesel Engine started.")


class Car:
    def __init__(self, engine: Engine):
        self.engine = engine
    
    def start_car(self):
        self.engine.start()
        print("Car is ready to go!")


# Example Usage
if __name__ == "__main__":
    petrol_car = Car(PetrolEngine())
    petrol_car.start_car()
    
    diesel_car = Car(DieselEngine())
    diesel_car.start_car()