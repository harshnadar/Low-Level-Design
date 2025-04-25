from interfaces import Subject, Observer

class WeatherStation(Subject):
    def __init__(self):
        self.observers = []
        self.temperature = 0.0
        self.humidity = 0.0
        self.pressure = 0.0

    def register_observer(self, observer):
        if not isinstance(observer, Observer):
            raise TypeError("Must implement Observer interface")
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for obs in self.observers:
            obs.update(self.temperature, self.humidity, self.pressure)

    def set_measurements(self, temp, humidity, pressure):
        self.temperature = temp
        self.humidity = humidity
        self.pressure = pressure
        self.notify_observers()