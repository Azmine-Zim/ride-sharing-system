"""
Data Persistence Module for Ride Sharing System
Handles saving and loading data to/from JSON files.
"""

import json
import os
from datetime import datetime


class DataManager:
    """
    Manages data persistence for the ride-sharing system.
    Saves and loads riders, drivers, and rides to/from JSON files.
    """
    
    def __init__(self, data_dir="data"):
        """Initialize data manager with data directory."""
        self.data_dir = data_dir
        self.riders_file = os.path.join(data_dir, "riders.json")
        self.drivers_file = os.path.join(data_dir, "drivers.json")
        self.rides_file = os.path.join(data_dir, "rides.json")
        self.company_file = os.path.join(data_dir, "company.json")
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def save_riders(self, riders):
        """Save riders to JSON file."""
        try:
            riders_data = []
            for rider in riders:
                rider_dict = {
                    'name': rider.name,
                    'email': rider.email,
                    'nid': rider.nid,
                    'current_location': rider.current_location,
                    'wallet': rider.wallet,
                    'ride_history_count': len(rider.ride_history),
                    'average_rating': getattr(rider, 'average_rating', 0.0),
                    'total_ratings': getattr(rider, 'total_ratings', 0)
                }
                riders_data.append(rider_dict)
            
            with open(self.riders_file, 'w') as f:
                json.dump(riders_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving riders: {e}")
            return False
    
    def load_riders(self):
        """Load riders from JSON file."""
        if not os.path.exists(self.riders_file):
            return []
        
        try:
            with open(self.riders_file, 'r') as f:
                riders_data = json.load(f)
            return riders_data
        except Exception as e:
            print(f"Error loading riders: {e}")
            return []
    
    def save_drivers(self, drivers):
        """Save drivers to JSON file."""
        try:
            drivers_data = []
            for driver in drivers:
                driver_dict = {
                    'name': driver.name,
                    'email': driver.email,
                    'nid': driver.nid,
                    'current_location': driver.current_location,
                    'wallet': driver.wallet,
                    'total_rides': driver.total_rides,
                    'is_available': driver.is_available,
                    'average_rating': getattr(driver, 'average_rating', 0.0),
                    'total_ratings': getattr(driver, 'total_ratings', 0),
                    'vehicle': {
                        'type': driver.vehicle.vehicle_type,
                        'license_plate': driver.vehicle.license_plate,
                        'rate': driver.vehicle.rate
                    } if driver.vehicle else None
                }
                drivers_data.append(driver_dict)
            
            with open(self.drivers_file, 'w') as f:
                json.dump(drivers_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving drivers: {e}")
            return False
    
    def load_drivers(self):
        """Load drivers from JSON file."""
        if not os.path.exists(self.drivers_file):
            return []
        
        try:
            with open(self.drivers_file, 'r') as f:
                drivers_data = json.load(f)
            return drivers_data
        except Exception as e:
            print(f"Error loading drivers: {e}")
            return []
    
    def save_rides(self, rides):
        """Save completed rides to JSON file."""
        try:
            rides_data = []
            for ride in rides:
                if ride.is_completed:
                    ride_dict = {
                        'start_location': ride.start_location,
                        'end_location': ride.end_location,
                        'distance': ride.distance,
                        'fare': ride.estimated_fare,
                        'vehicle_type': ride.vehicle.vehicle_type,
                        'rider_name': ride.rider.name if ride.rider else None,
                        'driver_name': ride.driver.name if ride.driver else None,
                        'start_time': ride.start_time.isoformat() if ride.start_time else None,
                        'end_time': ride.end_time.isoformat() if ride.end_time else None,
                        'status': 'completed'
                    }
                    rides_data.append(ride_dict)
            
            with open(self.rides_file, 'w') as f:
                json.dump(rides_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving rides: {e}")
            return False
    
    def load_rides(self):
        """Load rides from JSON file."""
        if not os.path.exists(self.rides_file):
            return []
        
        try:
            with open(self.rides_file, 'r') as f:
                rides_data = json.load(f)
            return rides_data
        except Exception as e:
            print(f"Error loading rides: {e}")
            return []
    
    def save_company_stats(self, company_name, total_rides):
        """Save company statistics."""
        try:
            company_data = {
                'company_name': company_name,
                'total_rides': total_rides,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.company_file, 'w') as f:
                json.dump(company_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving company stats: {e}")
            return False
    
    def load_company_stats(self):
        """Load company statistics."""
        if not os.path.exists(self.company_file):
            return {'company_name': 'QuickRide Bangladesh', 'total_rides': 0}
        
        try:
            with open(self.company_file, 'r') as f:
                company_data = json.load(f)
            return company_data
        except Exception as e:
            print(f"Error loading company stats: {e}")
            return {'company_name': 'QuickRide Bangladesh', 'total_rides': 0}
    
    def save_all(self, ride_sharing):
        """Save all data to files."""
        success = True
        success &= self.save_riders(ride_sharing.riders)
        success &= self.save_drivers(ride_sharing.drivers)
        success &= self.save_company_stats(ride_sharing.company_name, ride_sharing.total_rides)
        
        # Collect all completed rides from riders and drivers
        all_rides = []
        for rider in ride_sharing.riders:
            all_rides.extend(rider.ride_history)
        success &= self.save_rides(all_rides)
        
        return success
    
    def clear_all_data(self):
        """Clear all saved data files."""
        files = [self.riders_file, self.drivers_file, self.rides_file, self.company_file]
        for file in files:
            if os.path.exists(file):
                os.remove(file)
        print("\n✓ All saved data cleared!")
