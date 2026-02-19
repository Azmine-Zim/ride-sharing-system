from abc import ABC

class Vehicle(ABC):
    """
    Base class for all vehicles in the ride-sharing system.
    
    Attributes:
        speed (dict): Speed mapping for different vehicle types (km/h)
        vehicle_type (str): Type of vehicle (car, bike, cng)
        license_plate (str): License plate number
        rate (int): Rate per kilometer
        status (str): Current status of vehicle (available, in-ride)
    """
    speed = {
        'car': 50,
        'bike': 60,
        'cng': 15
    }
    
    def __init__(self, vehicle_type, license_plate, rate):
        """Initialize a vehicle with type, license plate, and rate."""
        self.vehicle_type = vehicle_type
        self.license_plate = license_plate
        self.rate = rate
        self.status = 'available'
    
    def __str__(self):
        """Return string representation of the vehicle."""
        return f"{self.vehicle_type.upper()} ({self.license_plate}) - Rate: {self.rate} BDT/km"


class Car(Vehicle):
    """Car vehicle for ride-sharing with 4-seater capacity."""
    
    def __init__(self, license_plate, rate=30):
        """Initialize a car with license plate and rate."""
        super().__init__('car', license_plate, rate)
        self.capacity = 4


class Bike(Vehicle):
    """Bike vehicle for ride-sharing with 2-seater capacity."""
    
    def __init__(self, license_plate, rate=20):
        """Initialize a bike with license plate and rate."""
        super().__init__('bike', license_plate, rate)
        self.capacity = 2


class CNG(Vehicle):
    """CNG (auto-rickshaw) vehicle for ride-sharing with 3-seater capacity."""
    
    def __init__(self, license_plate, rate=25):
        """Initialize a CNG with license plate and rate."""
        super().__init__('cng', license_plate, rate)
        self.capacity = 3



