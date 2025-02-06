from sun_position import SunPosition
from solar_panel import SolarPanel
from weather_service import WeatherService
from solar_optimizer import SolarOptimizer
from datetime import datetime
import os

def main():
    # Configuration
    latitude = 37.7749  # San Francisco
    longitude = -122.4194
    api_key = os.getenv('WEATHER_API_KEY')  # Get API key from environment variable
    
    # Initialize components
    sun_calculator = SunPosition(latitude, longitude)
    weather_service = WeatherService(api_key) if api_key else None
    optimizer = SolarOptimizer(sun_calculator, weather_service)
    
    # Set date for optimization
    date = datetime(2024, 6, 21)  # Summer solstice
    
    # Find optimal placement
    optimal_tilt, optimal_orientation, max_energy = optimizer.optimize_placement(date)
    
    print(f"Optimal tilt: {optimal_tilt}°")
    print(f"Optimal orientation: {optimal_orientation}°")
    print(f"Maximum daily energy: {max_energy/1000:.2f} kWh")
    
    # Simulate with optimal placement
    optimal_panel = SolarPanel(optimal_tilt, optimal_orientation)
    daily_output = optimizer.simulate_day(optimal_panel, date)
    
    # Visualize results
    optimizer.visualize_results(daily_output)

if __name__ == "__main__":
    main()