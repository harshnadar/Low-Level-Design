from interfaces import Observer, DisplayElement

# Observer 1: Current Conditions Display
class CurrentConditionsDisplay(Observer, DisplayElement):
    def __init__(self):
        self.temperature = 0.0
        self.humidity = 0.0

    def update(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.display()

    def display(self):
        print(f"Current Conditions: {self.temperature}°C, {self.humidity}% humidity")

# Observer 2: Statistics Display
class StatisticsDisplay(Observer, DisplayElement):
    def __init__(self):
        self.temps = []

    def update(self, temperature, humidity, pressure):
        self.temps.append(temperature)
        self.display()

    def display(self):
        avg = sum(self.temps)/len(self.temps)
        print(f"Temperature Stats: Avg {avg}°C | Max {max(self.temps)}°C")

# Observer 3: Forecast Display
class ForecastDisplay(Observer, DisplayElement):
    def update(self, temperature, humidity, pressure):
        self.last_pressure = pressure
        self.display()

    def display(self):
        trend = "Rising" if self.last_pressure > 1013 else "Falling"
        print(f"Forecast: Pressure {trend} - Expect {'sun' if trend == 'Rising' else 'rain'}")