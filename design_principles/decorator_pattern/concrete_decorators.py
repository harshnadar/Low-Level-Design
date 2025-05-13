from abc import ABC, abstractmethod
from decorator_base_class import CondimentDecorator

class Mocha(CondimentDecorator):
    def get_description(self) -> str:
        return f"{self.beverage.get_description()}, Mocha"
    
    def cost(self) -> float:
        return self.beverage.cost() + 0.49  # Add mocha cost

class Whip(CondimentDecorator):
    def get_description(self) -> str:
        return f"{self.beverage.get_description()}, Whip"
    
    def cost(self) -> float:
        return self.beverage.cost() + 0.39
