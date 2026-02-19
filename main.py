"""
Ride Sharing System - Interactive Console Application
A Python OOP-based ride-sharing platform with riders, drivers, and multiple vehicle types.
"""

from ride import Ride, RideRequest, RideMatching, RideSharing
from users import Rider, Driver
from vehicle import Car, Bike, CNG
from data_manager import DataManager
import os


def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print application header."""
    print("\n" + "="*60)
    print(f"{'🚗 RIDE SHARING SYSTEM 🚗':^60}")
    print("="*60)


def print_menu():
    """Display main menu options."""
    print("\n" + "-"*60)
    print("MAIN MENU")
    print("-"*60)
    print("1.  Register as Rider")
    print("2.  Register as Driver")
    print("3.  Request a Ride")
    print("4.  Complete Current Ride")
    print("5.  Cancel Current Ride")
    print("6.  View My Profile (Rider)")
    print("7.  View My Profile (Driver)")
    print("8.  Add Money to Wallet")
    print("9.  View Ride History")
    print("10. View All Riders")
    print("11. View All Drivers")
    print("12. View Top Rated Drivers")
    print("13. Search Drivers by Rating")
    print("14. View Company Stats")
    print("15. Save All Data")
    print("0.  Exit")
    print("-"*60)


def get_input(prompt, input_type=str):
    """Get and validate user input."""
    while True:
        try:
            value = input(prompt)
            if input_type == int:
                return int(value)
            elif input_type == float:
                return float(value)
            return value
        except ValueError:
            print(f"✗ Invalid input! Please enter a valid {input_type.__name__}.")


def find_rider_by_name(ride_sharing, name):
    """Find a rider by name."""
    for rider in ride_sharing.riders:
        if rider.name.lower() == name.lower():
            return rider
    return None


def find_driver_by_name(ride_sharing, name):
    """Find a driver by name."""
    for driver in ride_sharing.drivers:
        if driver.name.lower() == name.lower():
            return driver
    return None


def register_rider(ride_sharing):
    """Register a new rider."""
    print("\n" + "="*60)
    print(f"{'RIDER REGISTRATION':^60}")
    print("="*60)
    
    name = get_input("Enter your name: ")
    email = get_input("Enter your email: ")
    nid = get_input("Enter your NID: ")
    location = get_input("Enter your current location: ")
    initial_amount = get_input("Enter initial wallet amount (BDT): ", float)
    
    rider = Rider(name, email, nid, location, initial_amount)
    ride_sharing.add_rider(rider)


def register_driver(ride_sharing):
    """Register a new driver."""
    print("\n" + "="*60)
    print(f"{'DRIVER REGISTRATION':^60}")
    print("="*60)
    
    name = get_input("Enter your name: ")
    email = get_input("Enter your email: ")
    nid = get_input("Enter your NID: ")
    location = get_input("Enter your current location: ")
    
    # Vehicle selection
    print("\nSelect Your Vehicle Type:")
    print("  1. Car   (30 BDT/km)")
    print("  2. Bike  (20 BDT/km)")
    print("  3. CNG   (25 BDT/km)")
    
    vehicle_choice = get_input("Select vehicle type (1-3): ", int)
    license_plate = get_input("Enter vehicle license plate: ")
    
    # Create vehicle based on choice
    if vehicle_choice == 1:
        vehicle = Car(license_plate)
    elif vehicle_choice == 2:
        vehicle = Bike(license_plate)
    elif vehicle_choice == 3:
        vehicle = CNG(license_plate)
    else:
        print("\n✗ Invalid vehicle choice! Registration cancelled.")
        return
    
    driver = Driver(name, email, nid, location, vehicle)
    ride_sharing.add_driver(driver)


def request_ride(ride_sharing):
    """Request a ride."""
    if not ride_sharing.riders:
        print("\n✗ No riders registered! Please register as a rider first.")
        return
    
    if not ride_sharing.drivers:
        print("\n✗ No drivers available! Please register drivers first.")
        return
    
    print("\n" + "="*60)
    print(f"{'REQUEST A RIDE':^60}")
    print("="*60)
    
    rider_name = get_input("Enter your name (Rider): ")
    rider = find_rider_by_name(ride_sharing, rider_name)
    
    if not rider:
        print(f"\n✗ Rider '{rider_name}' not found! Please register first.")
        return
    
    destination = get_input("Enter destination: ")
    
    print("\nAvailable Vehicle Types:")
    print("  1. Car   (30 BDT/km + 50 BDT base fare)")
    print("  2. Bike  (20 BDT/km + 50 BDT base fare)")
    print("  3. CNG   (25 BDT/km + 50 BDT base fare)")
    
    vehicle_choice = get_input("Select vehicle type (1-3): ", int)
    
    vehicle_map = {1: 'car', 2: 'bike', 3: 'cng'}
    
    if vehicle_choice not in vehicle_map:
        print("\n✗ Invalid vehicle choice!")
        return
    
    vehicle_type = vehicle_map[vehicle_choice]
    ride = rider.request_ride(ride_sharing, destination, vehicle_type)
    
    if ride:
        rider.show_current_ride()


def complete_ride(ride_sharing):
    """Complete the current ride."""
    print("\n" + "="*60)
    print(f"{'COMPLETE RIDE':^60}")
    print("="*60)
    
    rider_name = get_input("Enter your name (Rider): ")
    rider = find_rider_by_name(ride_sharing, rider_name)
    
    if not rider:
        print(f"\n✗ Rider '{rider_name}' not found!")
        return
    
    if not rider.current_ride:
        print(f"\n✗ {rider_name} has no active ride!")
        return
    
    driver = rider.current_ride.driver
    driver.reach_destination(rider.current_ride)
    ride_sharing.total_rides += 1
    
    print(f"  Rider's Balance: {rider.wallet:.2f} BDT")
    print(f"  Driver's Balance: {driver.wallet:.2f} BDT")
    
    # Ask for rating
    print("\n" + "-"*50)
    rate_driver = get_input("Would you like to rate the driver? (y/n): ").lower()
    if rate_driver == 'y':
        rating = get_input("Rate your driver (1-5 stars): ", int)
        rider.rate_driver(rider.ride_history[-1], rating)


def cancel_ride(ride_sharing):
    """Cancel the current ride."""
    print("\n" + "="*60)
    print(f"{'CANCEL RIDE':^60}")
    print("="*60)
    
    rider_name = get_input("Enter your name (Rider): ")
    rider = find_rider_by_name(ride_sharing, rider_name)
    
    if not rider:
        print(f"\n✗ Rider '{rider_name}' not found!")
        return
    
    if not rider.current_ride:
        print(f"\n✗ {rider_name} has no active ride to cancel!")
        return
    
    confirm = get_input(f"Cancellation fee is {rider.current_ride.cancellation_fee:.2f} BDT. Confirm? (y/n): ").lower()
    if confirm == 'y':
        rider.current_ride.cancel_ride(cancelled_by='rider')


def view_rider_profile(ride_sharing):
    """View rider profile."""
    if not ride_sharing.riders:
        print("\n✗ No riders registered!")
        return
    
    rider_name = get_input("\nEnter your name (Rider): ")
    rider = find_rider_by_name(ride_sharing, rider_name)
    
    if rider:
        rider.display_profile()
    else:
        print(f"\n✗ Rider '{rider_name}' not found!")


def view_driver_profile(ride_sharing):
    """View driver profile."""
    if not ride_sharing.drivers:
        print("\n✗ No drivers registered!")
        return
    
    driver_name = get_input("\nEnter your name (Driver): ")
    driver = find_driver_by_name(ride_sharing, driver_name)
    
    if driver:
        driver.display_profile()
        driver.show_earnings()
    else:
        print(f"\n✗ Driver '{driver_name}' not found!")


def add_money_to_wallet(ride_sharing):
    """Add money to rider's wallet."""
    if not ride_sharing.riders:
        print("\n✗ No riders registered!")
        return
    
    print("\n" + "="*60)
    print(f"{'ADD MONEY TO WALLET':^60}")
    print("="*60)
    
    rider_name = get_input("Enter your name (Rider): ")
    rider = find_rider_by_name(ride_sharing, rider_name)
    
    if not rider:
        print(f"\n✗ Rider '{rider_name}' not found!")
        return
    
    amount = get_input("Enter amount to add (BDT): ", float)
    rider.load_cash(amount)


def view_ride_history(ride_sharing):
    """View ride history for a rider."""
    if not ride_sharing.riders:
        print("\n✗ No riders registered!")
        return
    
    rider_name = get_input("\nEnter your name (Rider): ")
    rider = find_rider_by_name(ride_sharing, rider_name)
    
    if rider:
        rider.show_ride_history()
    else:
        print(f"\n✗ Rider '{rider_name}' not found!")


def view_company_stats(ride_sharing):
    """View company statistics."""
    print("\n" + "="*60)
    print(f"{'COMPANY STATISTICS':^60}")
    print("="*60)
    print(f"Company Name  : {ride_sharing.company_name}")
    print(f"Total Riders  : {len(ride_sharing.riders)}")
    print(f"Total Drivers : {len(ride_sharing.drivers)}")
    print(f"Available Drivers: {len(ride_sharing.get_available_drivers())}")
    print(f"Completed Rides: {ride_sharing.total_rides}")
    print("="*60)


def search_drivers_by_rating(ride_sharing):
    """Search for drivers with minimum rating."""
    if not ride_sharing.drivers:
        print("\n✗ No drivers registered!")
        return
    
    print("\n" + "="*60)
    print(f"{'SEARCH DRIVERS BY RATING':^60}")
    print("="*60)
    
    min_rating = get_input("Enter minimum rating (1.0-5.0): ", float)
    if min_rating < 1.0 or min_rating > 5.0:
        print("\n✗ Rating must be between 1.0 and 5.0!")
        return
    
    ride_sharing.search_drivers_by_rating(min_rating)


def save_all_data(ride_sharing, data_manager):
    """Save all data to JSON files."""
    print("\n" + "="*60)
    print(f"{'SAVING DATA':^60}")
    print("="*60)
    
    if data_manager.save_all(ride_sharing):
        print("\n✓ All data saved successfully!")
        print(f"  Riders: {len(ride_sharing.riders)}")
        print(f"  Drivers: {len(ride_sharing.drivers)}")
        print(f"  Total Rides: {ride_sharing.total_rides}")
    else:
        print("\n✗ Error saving data!")


def load_saved_data(ride_sharing, data_manager):
    """Load previously saved data."""
    print("\n🔄 Loading saved data...")
    
    # Load company stats
    company_data = data_manager.load_company_stats()
    ride_sharing.total_rides = company_data.get('total_rides', 0)
    
    # Load riders
    riders_data = data_manager.load_riders()
    for rider_dict in riders_data:
        rider = Rider(
            rider_dict['name'],
            rider_dict['email'],
            rider_dict['nid'],
            rider_dict['current_location'],
            rider_dict['wallet']
        )
        rider.average_rating = rider_dict.get('average_rating', 0.0)
        rider.total_ratings = rider_dict.get('total_ratings', 0)
        ride_sharing.riders.append(rider)
    
    # Load drivers
    drivers_data = data_manager.load_drivers()
    for driver_dict in drivers_data:
        # Create vehicle if exists
        vehicle = None
        if driver_dict.get('vehicle'):
            v = driver_dict['vehicle']
            if v['type'] == 'car':
                vehicle = Car(v['license_plate'], v['rate'])
            elif v['type'] == 'bike':
                vehicle = Bike(v['license_plate'], v['rate'])
            elif v['type'] == 'cng':
                vehicle = CNG(v['license_plate'], v['rate'])
        
        driver = Driver(
            driver_dict['name'],
            driver_dict['email'],
            driver_dict['nid'],
            driver_dict['current_location'],
            vehicle
        )
        driver.wallet = driver_dict['wallet']
        driver.total_rides = driver_dict['total_rides']
        driver.is_available = driver_dict['is_available']
        driver.average_rating = driver_dict.get('average_rating', 0.0)
        driver.total_ratings = driver_dict.get('total_ratings', 0)
        ride_sharing.drivers.append(driver)
    
    if riders_data or drivers_data:
        print(f"✓ Loaded {len(riders_data)} riders and {len(drivers_data)} drivers")
        print(f"  Total completed rides: {ride_sharing.total_rides}")
    else:
        print("No saved data found. Starting fresh!")


def main():
    """Main application loop."""
    # Initialize ride-sharing company
    ride_sharing = RideSharing("QuickRide Bangladesh")
    data_manager = DataManager()
    
    # Try to load saved data
    load_option = get_input("\nLoad saved data? (y/n): ").lower()
    if load_option == 'y':
        load_saved_data(ride_sharing, data_manager)
    else:
        # Add some demo data
        demo_mode = get_input("Do you want to load demo data? (y/n): ").lower()
        
        if demo_mode == 'y':
            # Demo riders
            gablu = Rider("Gablu", "gablu@email.com", "765", "Mohakhali", 1000)
            rina = Rider("Rina", "rina@email.com", "123", "Dhanmondi", 1500)
            ride_sharing.riders.extend([gablu, rina])
            
            # Demo drivers with vehicles
            hablu = Driver("Hablu", "hablu@email.com", "456", "Gulshan", Car("DHK-1234"))
            karim = Driver("Karim", "karim@email.com", "789", "Banani", Bike("DHK-5678"))
            jamal = Driver("Jamal", "jamal@email.com", "321", "Uttara", CNG("DHK-9012"))
            
            # Set some ratings for demo
            hablu.average_rating = 4.5
            hablu.total_ratings = 10
            karim.average_rating = 4.8
            karim.total_ratings = 15
            jamal.average_rating = 4.2
            jamal.total_ratings = 8
            
            ride_sharing.drivers.extend([hablu, karim, jamal])
            
            print("\n✓ Demo data loaded successfully!")
            print(f"  - Riders: Gablu (1000 BDT), Rina (1500 BDT)")
            print(f"  - Drivers: Hablu (Car, 4.5⭐), Karim (Bike, 4.8⭐), Jamal (CNG, 4.2⭐)")
    
    # Main loop
    while True:
        print_header()
        print(f"\n{ride_sharing}")
        print_menu()
        
        choice = get_input("\nEnter your choice: ", int)
        
        if choice == 0:
            # Auto-save before exit
            print("\n💾 Saving data before exit...")
            save_all_data(ride_sharing, data_manager)
            
            print("\n" + "="*60)
            print(f"{'Thank you for using QuickRide Bangladesh!':^60}")
            print(f"{'Safe travels! 🚗':^60}")
            print("="*60 + "\n")
            break
        elif choice == 1:
            register_rider(ride_sharing)
        elif choice == 2:
            register_driver(ride_sharing)
        elif choice == 3:
            request_ride(ride_sharing)
        elif choice == 4:
            complete_ride(ride_sharing)
        elif choice == 5:
            cancel_ride(ride_sharing)
        elif choice == 6:
            view_rider_profile(ride_sharing)
        elif choice == 7:
            view_driver_profile(ride_sharing)
        elif choice == 8:
            add_money_to_wallet(ride_sharing)
        elif choice == 9:
            view_ride_history(ride_sharing)
        elif choice == 10:
            ride_sharing.show_all_riders()
        elif choice == 11:
            ride_sharing.show_all_drivers()
        elif choice == 12:
            ride_sharing.get_top_rated_drivers()
        elif choice == 13:
            search_drivers_by_rating(ride_sharing)
        elif choice == 14:
            view_company_stats(ride_sharing)
        elif choice == 15:
            save_all_data(ride_sharing, data_manager)
        else:
            print("\n✗ Invalid choice! Please select a valid option.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
