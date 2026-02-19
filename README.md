# 🚗 Ride Sharing System

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OOP](https://img.shields.io/badge/paradigm-OOP-green.svg)](https://en.wikipedia.org/wiki/Object-oriented_programming)

A comprehensive, feature-rich ride-sharing platform built with Python using Object-Oriented Programming (OOP) principles. This interactive console application simulates a real-world ride-sharing service like Uber, Pathao, or Lyft with persistent data storage, rating systems, and advanced matching algorithms.

## 🎯 Project Highlights

- **Full Data Persistence**: JSON-based storage system - your data is saved between sessions
- **Dual Rating System**: 5-star ratings for both riders and drivers with weighted averages
- **Smart Ride Matching**: Matches riders with best-rated drivers based on vehicle type
- **Cancellation Policy**: Rider cancellation with penalty fees, driver cancellation without fees
- **Comprehensive OOP**: Demonstrates abstraction, inheritance, encapsulation, and polymorphism
- **Production-Ready Features**: Error handling, input validation, search/filter capabilities
- **No External Dependencies**: Built entirely with Python standard library

## ✨ Features

### For Riders
- 👤 **User Registration**: Create a rider account with personal details
- 💰 **Digital Wallet**: Add and manage money in your wallet
- 🚕 **Request Rides**: Book rides with preferred vehicle types (Car, Bike, CNG)
- 📍 **Location Tracking**: Set and update current location
- 📊 **Ride History**: View all completed rides with details and ratings
- 🧾 **Current Ride Details**: Track ongoing ride information
- 💳 **Automatic Payment**: Seamless fare deduction from wallet
- ⭐ **Rating System**: Rate drivers after completing rides (1-5 stars)
- ❌ **Ride Cancellation**: Cancel rides with cancellation fee policy
- 📈 **Rating Profile**: View your average rating from drivers

### For Drivers
- 👨‍✈️ **Driver Registration**: Register as a driver with profile details and vehicle
- 🚗 **Vehicle Management**: Permanent vehicle assignment (Car, Bike, or CNG)
- 💵 **Earnings Tracking**: Monitor total earnings and ride count
- 🚦 **Availability Status**: Automatic status management (Available/Busy)
- 📈 **Ride History**: Track all completed rides
- 💰 **Wallet Management**: Automatic earnings credit after rides
- ⭐ **Rating System**: Rate riders and view your own driver rating
- 🏆 **Performance Tracking**: Track average rating and total ratings received

### System Features
- 🏢 **Company Management**: Track overall statistics
- 🔄 **Smart Matching**: Driver matching based on vehicle type and rating
- 💲 **Dynamic Pricing**: Calculate fares based on distance and vehicle type
- 📱 **Interactive Menu**: User-friendly console interface
- 🎲 **Demo Mode**: Pre-loaded sample data for testing
- 💾 **Data Persistence**: JSON-based save/load system for all data
- 🔍 **Search & Filter**: Search drivers by rating, filter top performers
- 📊 **Advanced Analytics**: View top-rated drivers, company statistics

## 🏗️ Project Structure

```
3_Ride_Sharing/
│
├── main.py          # Main application with interactive menu
├── ride.py          # Ride, RideSharing, and matching logic
├── users.py         # Rider and Driver classes
├── vehicle.py       # Vehicle hierarchy (Car, Bike, CNG)
├── data_manager.py  # JSON data persistence manager
├── data/            # Saved data directory (auto-created)
│   ├── riders.json  # Saved rider data
│   ├── drivers.json # Saved driver data
│   ├── rides.json   # Completed rides history
│   └── company.json # Company statistics
├── requirements.txt # Python dependencies
├── .gitignore       # Git ignore patterns
└── README.md        # Project documentation
```

## 🎯 Object-Oriented Design

### Class Hierarchy

```
User (Abstract Base Class)
│
├── Rider
│   ├── wallet
│   ├── current_ride
│   ├── ride_history
│   └── Methods: request_ride(), load_cash(), show_ride_history()
│
└── Driver
    ├── wallet
    ├── total_rides
    ├── is_available
    └── Methods: accept_ride(), reach_destination(), show_earnings()

Vehicle (Abstract Base Class)
│
├── Car (4-seater, 30 BDT/km)
├── Bike (2-seater, 20 BDT/km)
└── CNG (3-seater, 25 BDT/km)

RideSharing
├── riders[]
├── drivers[]
└── Methods: add_rider(), add_driver(), show_all_riders()

Ride
├── start_location
├── end_location
├── vehicle
├── estimated_fare
└── Methods: start_ride(), end_ride(), calculate_fare()
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ride-sharing-system.git
cd ride-sharing-system
```

2. Run the application:
```bash
python main.py
```

## 📖 How to Use

### Running the Application

1. **Start the program**:
   ```bash
   python main.py
   ```

2. **Choose demo mode** (recommended for first-time users):
   - Type `y` to load sample riders and drivers
   - Type `n` to start with an empty system

3. **Navigate the menu**: Enter the number corresponding to your desired action

### Example Usage Flow

#### Scenario 1: Complete Ride Journey (with demo data)

1. Start program and load demo data (`y`)
2. Select option `3` - Request a Ride
3. Enter rider name: `Gablu`
4. Enter destination: `Uttara`
5. Select vehicle: `1` (Car) - System matches best-rated car driver
6. View ride details and confirmation
7. Select option `4` - Complete Current Ride
8. Enter rider name: `Gablu`
9. See payment processing and updated balances
10. Rate the driver (1-5 stars)

#### Scenario 2: New User Registration

1. Select option `1` - Register as Rider
2. Enter your details (name, email, NID, location, initial wallet amount)
3. Select option `2` - Register as Driver
4. Enter driver details and choose vehicle type (Car/Bike/CNG)
5. Enter vehicle license plate
6. Now ready to accept rides or request them!

#### Scenario 3: Using Data Persistence

1. Start program, choose to load saved data (`y`)
2. All previous riders, drivers, and ride history loaded
3. Make changes, complete rides, update ratings
4. Data automatically saved when you exit
5. Or manually save anytime with option `15`

### Menu Options

| Option | Description |
|--------|-------------|
| 1 | Register as Rider |
| 2 | Register as Driver (with vehicle) |
| 3 | Request a Ride |
| 4 | Complete Current Ride (with rating) |
| 5 | Cancel Current Ride (with fee) |
| 6 | View My Profile (Rider) |
| 7 | View My Profile (Driver) |
| 8 | Add Money to Wallet |
| 9 | View Ride History |
| 10 | View All Riders |
| 11 | View All Drivers |
| 12 | View Top Rated Drivers |
| 13 | Search Drivers by Rating |
| 14 | View Company Stats |
| 15 | Save All Data |
| 0 | Exit (auto-saves data) |

## 💡 Key Concepts Demonstrated

### OOP Principles

1. **Abstraction**: `User` and `Vehicle` abstract base classes
2. **Inheritance**: `Rider` and `Driver` inherit from `User`; `Car`, `Bike`, `CNG` inherit from `Vehicle`
3. **Encapsulation**: Private data with public methods, data hiding
4. **Polymorphism**: Different vehicle types with shared interface

### Design Patterns

- **Factory Pattern**: Vehicle creation based on type
- **Strategy Pattern**: Different fare calculation strategies per vehicle
- **Repository Pattern**: DataManager for data persistence
- **Singleton Concept**: Single RideSharing company instance

### Advanced Features

- **Data Persistence**: JSON serialization and deserialization
- **Rating Algorithm**: Weighted average rating calculation
- **State Management**: Ride states (requested, in-progress, completed, cancelled)
- **Search Algorithms**: Filter and sort by multiple criteria

## 🎨 Features Breakdown

### Fare Calculation
```
Total Fare = Base Fare + (Distance × Vehicle Rate)

Base Fare: 50 BDT
Vehicle Rates:
  - Car:  30 BDT/km
  - Bike: 20 BDT/km
  - CNG:  25 BDT/km

Distance: Randomly generated (5-25 km)
```

### Rating System
- Both riders and drivers can rate each other (1-5 stars)
- Average rating calculated using weighted average formula
- Ratings displayed with star emojis (⭐) in profiles
- Top-rated drivers prioritized in ride matching
- Rating history tracked per user

### Ride Cancellation Policy
```
Cancellation Fee: 20 BDT

If cancelled by Rider:
  - Fee deducted from rider's wallet
  - Fee compensated to driver
  - Driver becomes available again

If cancelled by Driver:
  - No fee charged
  - Rider notified
```

### Wallet System
- Riders can add money to their wallet
- Automatic fare deduction upon ride completion
- Insufficient balance prevents ride booking
- Drivers receive automatic payment after completing rides
- All transactions tracked and displayed

### Ride Matching Algorithm
1. Filter available drivers by requested vehicle type
2. Select driver with highest rating
3. Create ride with driver's assigned vehicle
4. Update driver status to "Busy"
5. Confirm booking with fare estimate

### Data Persistence
- **Auto-save on exit**: All data automatically saved when exiting
- **Manual save option**: Save data anytime via menu
- **JSON format**: Human-readable data storage
- **Data restored**: Load previous session data on startup
- **Files saved**:
  - `riders.json` - All rider profiles and ratings
  - `drivers.json` - All driver profiles and vehicles
  - `rides.json` - Complete ride history
  - `company.json` - Company statistics

## 🛠️ Technical Details

### Technologies Used
- **Language**: Python 3.7+
- **Paradigm**: Object-Oriented Programming
- **Design Patterns**: Factory Pattern, Strategy Pattern
- **Data Storage**: JSON file-based persistence
- **Standard Libraries**: 
  - `datetime` - timestamp management
  - `random` - driver matching and distance generation
  - `os` - file system and console operations
  - `json` - data serialization/deserialization
  - `abc` - abstract base classes

### Error Handling
- Input validation for all user inputs
- Balance checking before ride confirmation
- Availability checking for drivers
- User existence verification

## 📊 Sample Output

```
============================================================
              🚗 RIDE SHARING SYSTEM 🚗
============================================================

🚗 QuickRide Bangladesh
   Riders: 2 | Drivers: 2 | Total Rides: 0

------------------------------------------------------------
MAIN MENU
------------------------------------------------------------
1.  Register as Rider
2.  Register as Driver
3.  Request a Ride
...

🔍 Searching for a car...

==================================================
           🎉 RIDE CONFIRMED!
==================================================

==================================================
            CURRENT RIDE DETAILS
==================================================
Rider         : Gablu
Driver        : Hablu
Vehicle       : CAR
License Plate : ABC123
From          : Mohakhali
To            : Uttara
Estimated Fare: 410.00 BDT
Status        : In Progress
==================================================
```

## ✅ Implemented Features (v2.0)

- [x] **Data Persistence**: JSON-based save/load system
- [x] **Rating System**: 5-star rating for both riders and drivers
- [x] **Ride Cancellation**: Cancellation with penalty fee system
- [x] **Vehicle Management**: Drivers own permanent vehicles
- [x] **Search & Filter**: Advanced search by rating
- [x] **Enhanced Matching**: Match drivers by vehicle type and rating
- [x] **Error Handling**: Comprehensive exception handling

## 🔮 Future Enhancements

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Real-time GPS tracking simulation with maps
- [ ] Detailed review system with comments
- [ ] Multiple payment methods (Card, Cash, Mobile Banking)
- [ ] Surge pricing during peak hours
- [ ] Ride scheduling and advance booking
- [ ] Driver earnings analytics dashboard
- [ ] Web/GUI interface with Flask or Django
- [ ] REST API implementation
- [ ] Unit tests and integration tests
- [ ] Distance calculation using coordinates
- [ ] Multi-city support
- [ ] Referral and promotion system

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**3rd Year Software Engineering Student**
- 🎓 Showcasing OOP mastery through practical application
- 💻 Building production-ready features with best practices
- 🌟 Open to collaboration and feedback

## 📬 Contact & Contribution

Want to contribute or have suggestions? 
- ⭐ Star this repository if you found it helpful
- 🐛 Report bugs via Issues
- 🔧 Submit Pull Requests for improvements
- 📧 Reach out for collaboration

### How to Contribute

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

**Happy Coding! 🚀**

*If you found this project helpful, please consider giving it a ⭐!*
