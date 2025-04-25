from concrete_subject import WeatherStation
from observers import CurrentConditionsDisplay, StatisticsDisplay, ForecastDisplay


def func():
    weather_station = WeatherStation()

    # Create displays (Observers)
    current_display = CurrentConditionsDisplay()
    stats_display = StatisticsDisplay()
    forecast_display = ForecastDisplay()

    # Register observers
    weather_station.register_observer(current_display)
    weather_station.register_observer(stats_display)
    weather_station.register_observer(forecast_display)

    # Simulate weather changes
    weather_station.set_measurements(25, 65, 1012)
    weather_station.set_measurements(26, 70, 1015)
    weather_station.set_measurements(24, 90, 1010)

if __name__ == "__main__":
    func()