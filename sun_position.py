import numpy as np
from datetime import datetime

class SunPosition:
    def __init__(self, latitude, longitude):
        """
        Initialize with location coordinates
        
        Args:
            latitude (float): Location latitude in degrees
            longitude (float): Location longitude in degrees
        """
        self.latitude = np.radians(latitude)
        self.longitude = np.radians(longitude)
        
    def calculate_sun_position(self, date_time):
        """
        Calculate sun's altitude and azimuth for a given date and time
        
        Args:
            date_time (datetime): Date and time for calculation
            
        Returns:
            tuple: (altitude, azimuth) in degrees
        """
        # Calculate day of year
        day_of_year = date_time.timetuple().tm_yday
        
        # Calculate solar declination
        declination = np.radians(23.45 * np.sin(np.radians(360/365 * (day_of_year - 81))))
        
        # Calculate hour angle
        hour_angle = np.radians(15 * (date_time.hour + date_time.minute/60 - 12))
        
        # Calculate solar altitude
        altitude = np.arcsin(
            np.sin(self.latitude) * np.sin(declination) +
            np.cos(self.latitude) * np.cos(declination) * np.cos(hour_angle)
        )
        
        # Calculate solar azimuth
        azimuth = np.arccos(
            (np.sin(declination) - np.sin(altitude) * np.sin(self.latitude)) /
            (np.cos(altitude) * np.cos(self.latitude))
        )
        
        # Convert to degrees
        altitude_deg = np.degrees(altitude)
        azimuth_deg = np.degrees(azimuth)
        
        # Adjust azimuth based on time of day
        if hour_angle > 0:
            azimuth_deg = 360 - azimuth_deg
            
        return altitude_deg, azimuth_deg