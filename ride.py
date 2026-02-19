from datetime import datetime
import random
from vehicle import Car, Bike, CNG


class RideSharing:
    """
    Main ride-sharing company class that manages riders and drivers.
    
    Attributes:
        company_name (str): Name of the company
        riders (list): List of registered riders
        drivers (list): List of registered drivers
        total_rides (int): Total completed rides
    """
    
    def __init__(self, company_name):
        """Initialize the ride-sharing company."""
        self.company_name = company_name
        self.riders = []
        self.drivers = []
        self.total_rides = 0
    
    def add_rider(self, rider):
        """Register a new rider."""
        self.riders.append(rider)
        print(f"\n✓ Rider '{rider.name}' registered successfully!")
    
    def add_driver(self, driver):
        """Register a new driver."""
        self.drivers.append(driver)
        print(f"\n✓ Driver '{driver.name}' registered successfully!")
    
    def get_available_drivers(self):
        """Return list of available drivers."""
        return [driver for driver in self.drivers if driver.is_available]
    
    def show_all_riders(self):
        """Display all registered riders."""
        if not self.riders:
            print("\n✗ No riders registered yet!")
            return
        
        print("\n" + "="*60)
        print(f"{'ALL REGISTERED RIDERS':^60}")
        print("="*60)
        for idx, rider in enumerate(self.riders, 1):
            print(f"{idx}. {rider.name} - {rider.email} - Balance: {rider.wallet:.2f} BDT")
        print("="*60)
    
    def show_all_drivers(self):
        """Display all registered drivers."""
        if not self.drivers:
            print("\n✗ No drivers registered yet!")
            return
        
        print("\n" + "="*60)
        print(f"{'ALL REGISTERED DRIVERS':^60}")
        print("="*60)
        for idx, driver in enumerate(self.drivers, 1):
            status = "Available" if driver.is_available else "Busy"
            vehicle_info = f"{driver.vehicle.vehicle_type.upper()} ({driver.vehicle.license_plate})" if driver.vehicle else "No vehicle"
            rating_stars = "⭐" * int(driver.average_rating) + "☆" * (5 - int(driver.average_rating))
            print(f"{idx}. {driver.name} - {driver.email}")
            print(f"   Status: {status} | Vehicle: {vehicle_info}")
            print(f"   Rating: {driver.average_rating:.1f}/5.0 {rating_stars}")
        print("="*60)
    
    def search_drivers_by_rating(self, min_rating=4.0):
        """Search for drivers with rating above specified threshold."""
        top_drivers = [d for d in self.drivers if d.average_rating >= min_rating]
        
        if not top_drivers:
            print(f"\n✗ No drivers found with rating >= {min_rating}")
            return []
        
        print("\n" + "="*60)
        print(f"{'DRIVERS WITH RATING >= ' + str(min_rating):^60}")
        print("="*60)
        
        # Sort by rating descending
        top_drivers.sort(key=lambda d: d.average_rating, reverse=True)
        
        for idx, driver in enumerate(top_drivers, 1):
            rating_stars = "⭐" * int(driver.average_rating) + "☆" * (5 - int(driver.average_rating))
            vehicle_info = f"{driver.vehicle.vehicle_type.upper()}" if driver.vehicle else "No vehicle"
            print(f"{idx}. {driver.name} - Rating: {driver.average_rating:.1f}/5.0 {rating_stars}")
            print(f"   Vehicle: {vehicle_info} | Total Rides: {driver.total_rides}")
        print("="*60)
        
        return top_drivers
    
    def search_riders_by_name(self, name):
        """Search for riders by name (partial match)."""
        matches = [r for r in self.riders if name.lower() in r.name.lower()]
        
        if not matches:
            print(f"\n✗ No riders found matching '{name}'")
            return []
        
        print("\n" + "="*60)
        print(f"{'SEARCH RESULTS FOR: ' + name:^60}")
        print("="*60)
        for idx, rider in enumerate(matches, 1):
            print(f"{idx}. {rider.name} - {rider.email}")
            print(f"   Balance: {rider.wallet:.2f} BDT | Rides: {len(rider.ride_history)}")
        print("="*60)
        
        return matches
    
    def get_top_rated_drivers(self, limit=5):
        """Get top rated drivers."""
        if not self.drivers:
            print("\n✗ No drivers registered yet!")
            return []
        
        # Filter drivers with at least one rating
        rated_drivers = [d for d in self.drivers if d.total_ratings > 0]
        
        if not rated_drivers:
            print("\n✗ No drivers have been rated yet!")
            return []
        
        # Sort by rating and total rides
        top_drivers = sorted(rated_drivers, 
                            key=lambda d: (d.average_rating, d.total_rides), 
                            reverse=True)[:limit]
        
        print("\n" + "="*60)
        print(f"{'TOP RATED DRIVERS':^60}")
        print("="*60)
        for idx, driver in enumerate(top_drivers, 1):
            rating_stars = "⭐" * int(driver.average_rating) + "☆" * (5 - int(driver.average_rating))
            vehicle_info = f"{driver.vehicle.vehicle_type.upper()}" if driver.vehicle else "No vehicle"
            print(f"{idx}. {driver.name}")
            print(f"   Rating: {driver.average_rating:.1f}/5.0 {rating_stars} ({driver.total_ratings} ratings)")
            print(f"   Vehicle: {vehicle_info} | Total Rides: {driver.total_rides}")
        print("="*60)
        
        return top_drivers
    
    def __str__(self):
        """Return string representation of the company."""
        return (f"🚗 {self.company_name}\n"
                f"   Riders: {len(self.riders)} | "
                f"Drivers: {len(self.drivers)} | "
                f"Total Rides: {self.total_rides}")


class Ride:
    """
    Represents a single ride in the system.
    
    Attributes:
        start_location (str): Starting point of the ride
        end_location (str): Destination of the ride
        vehicle: Vehicle assigned for the ride
        driver: Driver assigned to the ride
        rider: Rider who requested the ride
        distance (float): Distance in kilometers
        estimated_fare (float): Calculated fare
        is_completed (bool): Ride completion status
        is_cancelled (bool): Ride cancellation status
        cancellation_fee (float): Fee charged for cancellation
        rating (int): Rating given by rider to driver
    """
    
    CANCELLATION_FEE = 20  # BDT
    
    def __init__(self, start_location, end_location, vehicle, distance=None):
        """Initialize a ride with locations and vehicle."""
        self.start_location = start_location
        self.end_location = end_location
        self.driver = None
        self.rider = None
        self.start_time = None
        self.end_time = None
        self.vehicle = vehicle
        self.distance = distance if distance else random.randint(5, 25)  # Random distance 5-25 km
        self.estimated_fare = self.calculate_fare()
        self.is_completed = False
        self.is_cancelled = False
        self.cancellation_fee = self.CANCELLATION_FEE
        self.rating = None
    
    def set_driver(self, driver):
        """Assign a driver to the ride."""
        self.driver = driver
    
    def start_ride(self):
        """Start the ride and record start time."""
        self.start_time = datetime.now()
        print(f"\n🚗 Ride started at {self.start_time.strftime('%H:%M:%S')}")
    
    def end_ride(self):
        """Complete the ride and process payment."""
        self.end_time = datetime.now()
        self.is_completed = True
        
        # Process payment
        self.rider.wallet -= self.estimated_fare
        self.driver.wallet += self.estimated_fare
        
        # Add to ride history
        self.rider.ride_history.append(self)
        
        # Clear current ride
        self.rider.current_ride = None
        
        duration = (self.end_time - self.start_time).seconds // 60
        print(f"\n✓ Ride completed!")
        print(f"  Duration: {duration} minutes")
        print(f"  Distance: {self.distance} km")
        print(f"  Fare: {self.estimated_fare:.2f} BDT")
    
    def calculate_fare(self):
        """Calculate fare based on distance and vehicle type."""
        base_fare = 50  # Base fare in BDT
        fare = base_fare + (self.distance * self.vehicle.rate)
        return round(fare, 2)
    
    def cancel_ride(self, cancelled_by='rider'):
        """Cancel the ride and charge cancellation fee."""
        if self.is_completed:
            print("\n✗ Cannot cancel a completed ride!")
            return False
        
        if self.is_cancelled:
            print("\n✗ Ride is already cancelled!")
            return False
        
        self.is_cancelled = True
        self.end_time = datetime.now()
        
        if cancelled_by == 'rider':
            # Charge cancellation fee to rider
            if self.rider.wallet >= self.cancellation_fee:
                self.rider.wallet -= self.cancellation_fee
                if self.driver:
                    self.driver.wallet += self.cancellation_fee
                    print(f"\n✓ Ride cancelled! Cancellation fee of {self.cancellation_fee:.2f} BDT charged.")
                    print(f"  Compensated to driver: {self.driver.name}")
            else:
                print(f"\n✓ Ride cancelled! Insufficient balance for cancellation fee.")
        else:
            # Driver cancelled - no fee
            print("\n✓ Ride cancelled by driver. No cancellation fee.")
        
        # Make driver available again
        if self.driver:
            self.driver.is_available = True
        
def __repr__(self):
        """Return string representation of the ride."""
        status = "Cancelled" if self.is_cancelled else ("Completed" if self.is_completed else "In Progress")
        return f"Ride: {self.start_location} → {self.end_location} ({self.distance} km) - {status}"


class RideRequest:
    """
    Represents a ride request from a rider.
    
    Attributes:
        rider: Rider who made the request
        end_location (str): Requested destination
    """
    
    def __init__(self, rider, end_location):
        """Initialize a ride request."""
        self.rider = rider
        self.end_location = end_location


class RideMatching:
    """
    Handles matching riders with available drivers.
    
    Attributes:
        available_drivers (list): List of available drivers
    """
    
    def __init__(self, drivers):
        """Initialize ride matching with available drivers."""
        self.available_drivers = [d for d in drivers if d.is_available]
    
    def find_driver(self, ride_request, vehicle_type):
        """Find an available driver with the specified vehicle type."""
        if not self.available_drivers:
            return None
        
        # Filter drivers by vehicle type and availability
        suitable_drivers = []
        for driver in self.available_drivers:
            if driver.vehicle and driver.vehicle.vehicle_type == vehicle_type.lower():
                suitable_drivers.append(driver)
        
        if not suitable_drivers:
            print(f"\n✗ No {vehicle_type} drivers available at the moment.")
            return None
        
        # Select best driver (by rating)
        best_driver = max(suitable_drivers, key=lambda d: d.average_rating)
        
        # Create ride with driver's vehicle
        ride = Ride(ride_request.rider.current_location, 
                   ride_request.end_location, 
                   best_driver.vehicle)
        best_driver.accept_ride(ride)
        
        return ride

    