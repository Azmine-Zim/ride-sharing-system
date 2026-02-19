from abc import ABC, abstractmethod
from ride import RideRequest, RideMatching


class User(ABC):
    """
    Abstract base class for all users in the ride-sharing system.
    
    Attributes:
        name (str): User's full name
        email (str): User's email address
        nid (str): National ID number
        wallet (float): Current wallet balance
    """
    
    def __init__(self, name, email, nid):
        """Initialize a user with name, email, and NID."""
        self.name = name
        self.email = email
        self.nid = nid
        self.wallet = 0

    @abstractmethod
    def display_profile(self):
        """Display user profile information."""
        raise NotImplementedError


class Rider(User):
    """
    Rider class representing a passenger in the ride-sharing system.
    
    Attributes:
        current_ride: Currently active ride
        current_location (str): Current location of the rider
        ride_history (list): List of completed rides
        average_rating (float): Average rating received from drivers
        total_ratings (int): Total number of ratings received
    """
    
    def __init__(self, name, email, nid, current_location, initial_amount=0):
        """Initialize a rider with location and initial wallet amount."""
        super().__init__(name, email, nid)
        self.current_ride = None
        self.wallet = initial_amount
        self.current_location = current_location
        self.ride_history = []
        self.average_rating = 0.0
        self.total_ratings = 0

    def display_profile(self):
        """Display rider profile information."""
        print("\n" + "="*50)
        print(f"{'RIDER PROFILE':^50}")
        print("="*50)
        print(f"Name          : {self.name}")
        print(f"Email         : {self.email}")
        print(f"NID           : {self.nid}")
        print(f"Location      : {self.current_location}")
        print(f"Wallet Balance: {self.wallet:.2f} BDT")
        print(f"Total Rides   : {len(self.ride_history)}")
        rating_stars = "⭐" * int(self.average_rating) + "☆" * (5 - int(self.average_rating))
        print(f"Rating        : {self.average_rating:.1f}/5.0 {rating_stars} ({self.total_ratings} ratings)")
        print("="*50)

    def load_cash(self, amount):
        """Add money to the rider's wallet."""
        if amount > 0:
            self.wallet += amount
            print(f"\n✓ Successfully added {amount:.2f} BDT to your wallet!")
            print(f"  New Balance: {self.wallet:.2f} BDT")
            return True
        else:
            print("\n✗ Error: Amount must be greater than 0")
            return False
    
    def update_location(self, current_location):
        """Update the rider's current location."""
        self.current_location = current_location
        print(f"\n✓ Location updated to: {current_location}")

    def request_ride(self, ride_sharing, destination, vehicle_type):
        """Request a ride to the destination with specified vehicle type."""
        try:
            if self.current_ride and not self.current_ride.is_completed and not self.current_ride.is_cancelled:
                print("\n✗ You already have an active ride!")
                return None
            
            print(f"\n🔍 Searching for a {vehicle_type}...")
            ride_request = RideRequest(self, destination)
            ride_matching = RideMatching(ride_sharing.drivers)
            ride = ride_matching.find_driver(ride_request, vehicle_type)
            
            if ride:
                if self.wallet >= ride.estimated_fare:
                    ride.rider = self
                    self.current_ride = ride
                    print("\n" + "="*50)
                    print(f"{'🎉 RIDE CONFIRMED!':^50}")
                    print("="*50)
                    return ride
                else:
                    print(f"\n✗ Insufficient balance! Need {ride.estimated_fare:.2f} BDT")
                    print(f"  Your balance: {self.wallet:.2f} BDT")
                    print(f"  Please load {ride.estimated_fare - self.wallet:.2f} BDT more")
                    return None
            else:
                print(f"\n✗ Sorry! No {vehicle_type} drivers available at the moment.")
                return None
        except Exception as e:
            print(f"\n✗ Error requesting ride: {e}")
            return None

    def show_current_ride(self):
        """Display current ride details."""
        if not self.current_ride:
            print("\n✗ No active ride found!")
            return
        
        ride = self.current_ride
        print("\n" + "="*50)
        print(f"{'CURRENT RIDE DETAILS':^50}")
        print("="*50)
        print(f"Rider         : {self.name}")
        print(f"Driver        : {ride.driver.name if ride.driver else 'N/A'}")
        print(f"Vehicle       : {ride.vehicle.vehicle_type.upper()}")
        print(f"License Plate : {ride.vehicle.license_plate}")
        print(f"From          : {ride.start_location}")
        print(f"To            : {ride.end_location}")
        print(f"Estimated Fare: {ride.estimated_fare:.2f} BDT")
        print(f"Status        : {'Completed' if ride.is_completed else 'In Progress'}")
        print("="*50)

    def show_ride_history(self):
        """Display all completed rides."""
        if not self.ride_history:
            print("\n✗ No ride history available.")
            return
        
        print("\n" + "="*60)
        print(f"{'RIDE HISTORY':^60}")
        print("="*60)
        for idx, ride in enumerate(self.ride_history, 1):
            print(f"\nRide #{idx}")
            print(f"  From: {ride.start_location} → To: {ride.end_location}")
            print(f"  Driver: {ride.driver.name}")
            print(f"  Vehicle: {ride.vehicle.vehicle_type.upper()}")
            if hasattr(ride, 'rating') and ride.rating:
                print(f"  Your Rating: {'⭐' * ride.rating}")
        print("="*60)
    
    def rate_driver(self, ride, rating):
        """Rate a driver after completing a ride."""
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                print("\n✗ Rating must be between 1 and 5!")
                return False
            
            ride.rating = rating
            
            # Update driver's average rating
            driver = ride.driver
            driver.total_ratings += 1
            driver.average_rating = ((driver.average_rating * (driver.total_ratings - 1)) + rating) / driver.total_ratings
            
            print(f"\n✓ You rated {driver.name} {rating} stars!")
            return True
        except ValueError:
            print("\n✗ Invalid rating! Please enter a number between 1 and 5.")
            return False


class Driver(User):
    """
    Driver class representing a driver in the ride-sharing system.
    
    Attributes:
        current_location (str): Current location of the driver
        vehicle: Assigned vehicle
        total_rides (int): Total number of completed rides
        is_available (bool): Availability status
        ride_history (list): List of completed rides
        average_rating (float): Average rating received from riders
        total_ratings (int): Total number of ratings received
    """
    
    def __init__(self, name, email, nid, current_location, vehicle=None):
        """Initialize a driver with location and optional vehicle."""
        super().__init__(name, email, nid)
        self.current_location = current_location
        self.vehicle = vehicle
        self.total_rides = 0
        self.is_available = True
        self.ride_history = []
        self.average_rating = 0.0
        self.total_ratings = 0
    
    def display_profile(self):
        """Display driver profile information."""
        print("\n" + "="*50)
        print(f"{'DRIVER PROFILE':^50}")
        print("="*50)
        print(f"Name          : {self.name}")
        print(f"Email         : {self.email}")
        print(f"NID           : {self.nid}")
        print(f"Location      : {self.current_location}")
        print(f"Wallet Balance: {self.wallet:.2f} BDT")
        print(f"Total Rides   : {self.total_rides}")
        print(f"Vehicle       : {self.vehicle if self.vehicle else 'Not assigned'}")
        print(f"Status        : {'Available' if self.is_available else 'Busy'}")
        rating_stars = "⭐" * int(self.average_rating) + "☆" * (5 - int(self.average_rating))
        print(f"Rating        : {self.average_rating:.1f}/5.0 {rating_stars} ({self.total_ratings} ratings)")
        print("="*50)
    
    def accept_ride(self, ride):
        """Accept a ride request."""
        ride.start_ride()
        ride.set_driver(self)
        self.is_available = False
    
    def reach_destination(self, ride):
        """Mark ride as completed and update earnings."""
        ride.end_ride()
        self.total_rides += 1
        self.is_available = True
        self.ride_history.append(ride)
        print(f"\n✓ Ride completed! Earned {ride.estimated_fare:.2f} BDT")
    
    def show_earnings(self):
        """Display driver's earnings summary."""
        print("\n" + "="*50)
        print(f"{'EARNINGS SUMMARY':^50}")
        print("="*50)
        print(f"Total Rides   : {self.total_rides}")
        print(f"Total Earnings: {self.wallet:.2f} BDT")
        if self.total_rides > 0:
            avg_earni    
    def set_vehicle(self, vehicle):
        """Assign a vehicle to the driver."""
        self.vehicle = vehicle
        print(f"\n✓ Vehicle {vehicle.vehicle_type.upper()} ({vehicle.license_plate}) assigned to {self.name}")
    
    def rate_rider(self, ride, rating):
        """Rate a rider after completing a ride."""
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                print("\n✗ Rating must be between 1 and 5!")
                return False
            
            # Update rider's average rating
            rider = ride.rider
            rider.total_ratings += 1
            rider.average_rating = ((rider.average_rating * (rider.total_ratings - 1)) + rating) / rider.total_ratings
            
            print(f"\n✓ You rated {rider.name} {rating} stars!")
            return True
        except ValueError:
            print("\n✗ Invalid rating! Please enter a number between 1 and 5.")
            return False
    