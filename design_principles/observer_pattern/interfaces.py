from abc import ABC, abstractmethod

# Subject Interface (Publisher)
class Subject(ABC):
    @abstractmethod
    def register_observer(self, observer):
        pass

    @abstractmethod
    def remove_observer(self, observer):
        pass

    @abstractmethod
    def notify_observers(self):
        pass

# Observer Interface (Subscriber)
class Observer(ABC):
    @abstractmethod
    def update(self, temperature: float, humidity: float, pressure: float):
        pass

# Optional Display Interface (From Book Example)
class DisplayElement(ABC):
    @abstractmethod
    def display(self):
        pass