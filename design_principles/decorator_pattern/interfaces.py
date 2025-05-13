from abc import ABC, abstractmethod

class Beverage(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def cost(self) -> float:
        pass

class DarkRoast(Beverage):
    def get_description(self) -> str:
        return "Dark Roast Coffee"
    
    def cost(self) -> float:
        return 2.99  # Base price
