from abc import ABC, abstractmethod
from interfaces import Beverage

class CondimentDecorator(Beverage):
    def __init__(self, beverage: Beverage):
        self.beverage = beverage  # Reference to wrapped object

    @abstractmethod
    def get_description(self) -> str:
        pass  # To be implemented by concrete decorators
