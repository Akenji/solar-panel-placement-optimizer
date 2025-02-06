import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from solar_panel import SolarPanel


class SolarOptimizer:
    def __init__(self, sun_position, weather_service=None):
        """
        Initialize optimizer
        
        Args:
            sun_position (SunPosition): SunPosition calculator instance
            weather_service (WeatherService): Optional WeatherService instance
        """
        self.sun_calculator = sun_position
        self.weather_service = weather_service
        self.results = []
        
    def simulate_day(self, panel, date, time_step_minutes=30):
        """
        Simulate panel output over a day
        
        Args:
            panel (SolarPanel): Solar panel object
            date (datetime): Date to simulate
            time_step_minutes (int): Time step for simulation
            
        Returns:
            list: Hourly power outputs
        """
        daily_output = []
        
        # Simulate for each time step
        for hour in range(24):
            for minute in range(0, 60, time_step_minutes):
                time = date.replace(hour=hour, minute=minute)
                altitude, azimuth = self.sun_calculator.calculate_sun_position(time)
                
                # Get weather data if available
                weather_data = None
                if self.weather_service:
                    weather_data = self.weather_service.get_weather_data(
                        np.degrees(self.sun_calculator.latitude),
                        np.degrees(self.sun_calculator.longitude),
                        time
                    )
                
                if altitude > 0:  # Only calculate during daylight
                    power = panel.calculate_power_output(altitude, azimuth, weather_data)
                    daily_output.append({
                        'time': time,
                        'power': power,
                        'altitude': altitude,
                        'azimuth': azimuth,
                        'weather': weather_data
                    })
                    
        return daily_output
    
    def optimize_placement(self, date, tilt_range=(0, 90), orientation_range=(0, 360)):
        """
        Find optimal panel placement
        
        Args:
            date (datetime): Date to optimize for
            tilt_range (tuple): Range of tilt angles to test
            orientation_range (tuple): Range of orientation angles to test
            
        Returns:
            tuple: (optimal_tilt, optimal_orientation, max_daily_energy)
        """
        max_energy = 0
        optimal_tilt = 0
        optimal_orientation = 0
        results = []
        
        # Test different combinations
        for tilt in range(tilt_range[0], tilt_range[1], 5):
            for orientation in range(orientation_range[0], orientation_range[1], 5):
                panel = SolarPanel(tilt, orientation)
                daily_output = self.simulate_day(panel, date)
                
                # Calculate total daily energy
                daily_energy = sum(record['power'] for record in daily_output)
                results.append({
                    'tilt': tilt,
                    'orientation': orientation,
                    'energy': daily_energy
                })
                
                if daily_energy > max_energy:
                    max_energy = daily_energy
                    optimal_tilt = tilt
                    optimal_orientation = orientation
        
        self.results = results
        return optimal_tilt, optimal_orientation, max_energy
    
    def visualize_results(self, daily_output):
        """
        Create visualization of daily power output
        
        Args:
            daily_output (list): Simulation results
        """
        # Daily power output plot
        plt.figure(figsize=(12, 6))
        times = [record['time'] for record in daily_output]
        powers = [record['power'] for record in daily_output]
        
        plt.plot(times, powers)
        plt.title('Solar Panel Power Output Over Day')
        plt.xlabel('Time')
        plt.ylabel('Power Output (W)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        # Optimization results heat map
        if self.results:
            df = pd.DataFrame(self.results)
            pivot_table = df.pivot_table(
                values='energy', 
                index='tilt', 
                columns='orientation', 
                aggfunc='first'
            )
            
            plt.figure(figsize=(12, 8))
            plt.imshow(pivot_table, cmap='viridis', aspect='auto')
            plt.colorbar(label='Daily Energy (Wh)')
            plt.title('Energy Production by Panel Orientation and Tilt')
            plt.xlabel('Orientation (degrees)')
            plt.ylabel('Tilt (degrees)')
            plt.tight_layout()
            plt.show()