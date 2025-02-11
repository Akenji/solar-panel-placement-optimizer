import numpy as np

class SolarPanel:
    def __init__(self, tilt, orientation, efficiency=0.2, area=1.6):
        """
        Initialize solar panel properties
        
        Args:
            tilt (float): Panel tilt angle in degrees
            orientation (float): Panel orientation (azimuth) in degrees
            efficiency (float): Panel efficiency (default 20%)
            area (float): Panel area in square meters
        """
        self.tilt = np.radians(tilt)
        self.orientation = np.radians(orientation)
        self.efficiency = efficiency
        self.area = area
        
    def calculate_power_output(self, sun_altitude, sun_azimuth, weather_data=None):
        """
        Calculate power output based on sun position and weather conditions
        
        Args:
            sun_altitude (float): Sun's altitude in degrees
            sun_azimuth (float): Sun's azimuth in degrees
            weather_data (dict): Optional weather data including cloud cover and temperature
            
        Returns:
            float: Power output in watts
        """
        # Base solar intensity (W/m²)
        solar_intensity = 1000
        
        # Adjust for weather conditions if available
        if weather_data:
            cloud_factor = 1 - (weather_data.get('cloud_cover', 0) / 100)
            temp_coefficient = 1 - (0.004 * (weather_data.get('temperature', 25) - 25))  # Temperature coefficient
            solar_intensity *= cloud_factor * temp_coefficient
        
        # Convert sun position to radians
        sun_altitude_rad = np.radians(sun_altitude)
        sun_azimuth_rad = np.radians(sun_azimuth)
        
        # Calculate incidence angle using spherical trigonometry
        cos_incidence = (
            np.cos(sun_altitude_rad) * np.sin(self.tilt) * 
            np.cos(sun_azimuth_rad - self.orientation) +
            np.sin(sun_altitude_rad) * np.cos(self.tilt)
        )
        
        # Calculate power output
        if cos_incidence > 0:
            # Add air mass effect
            air_mass = 1 / (np.sin(sun_altitude_rad) + 0.50572 * (6.07995 + sun_altitude)**-1.6364)
            atmospheric_loss = 0.7 ** air_mass
            
            power = solar_intensity * cos_incidence * self.efficiency * self.area * atmospheric_loss
            return power
        return 0