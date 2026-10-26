# 🇵🇰 Pakistan Ride
## Smart Map + AI Fare Prediction

Pakistan Ride is a Python-based ride-booking application designed to make local transportation smarter, more accessible, and easier to manage. The application combines interactive mapping, location selection, distance estimation, estimated travel times, and AI-style fare prediction using configurable fare rules and historical completed rides.

## 🚀 Key Features

### 🗺️ Interactive Smart Map
- Integrated `TkinterMapView` with OpenStreetMap.
- Select pickup and destination locations by clicking on the map.
- Place markers for selected locations.
- Search predefined starter locations across Pakistan.
- Display geographic coordinates for distance calculations.
- Support offline map tiles when properly configured.

### 📍 Distance Estimation
- Calculate approximate distances using pickup and destination coordinates.
- Use geographic distance estimates in fare calculations.
- Support distance-based ride estimates.

### ⏱️ Estimated Travel Time
- Estimate journey duration based on trip distance.
- Apply configured assumptions for different ride types.
- Display approximate travel time to help passengers plan their trips.

### 🤖 AI-Style Fare Prediction
- Calculate estimated fares using configurable fare rules.
- Use historical completed rides to support fare estimation.
- Display an estimated fare range.
- Provide an indicative prediction confidence level.
- Store the predicted fare with the associated booking.

The prediction system is data-driven, but it should only be described as machine learning if a trained model is actually implemented.

### 🚖 Ride Booking
- Support ride-booking workflows.
- Associate pickup and destination details with bookings.
- Store predicted fares with ride records.
- Support ride management according to the implemented user roles.

### 👥 User Roles
The application includes separate demo accounts for passengers, drivers, and administrators.

| Role | Username | Password |
|---|---|---|
| Passenger | `passenger` | `passenger123` |
| Driver | `driver` | `driver123` |
| Admin | `admin` | `admin123` |

These credentials are for demonstration purposes only.

## 🛠️ Technology Stack

**Frontend and GUI**
- Tkinter
- TkinterMapView
- OpenStreetMap

**Backend and application logic**
- Python
- Fare calculation and prediction logic
- Distance and ETA estimation
- Booking management
- Authentication and role management

**Data and mapping**
- Historical completed ride data
- Geographic coordinates
- Configurable fare rules
- Map tiles and location lookup

The database technology should be specified according to the actual implementation.

## ⚙️ Installation on Windows

### 1. Navigate to the project directory

```bash
cd path\to\Pakistan-Ride
```

Replace the example path with your actual project folder.

### 2. Create a virtual environment

```bash
py -m venv .venv
```

### 3. Activate the environment

```bash
.venv\Scripts\activate
```

### 4. Install the dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python main.py
```

## 🧠 How Fare Prediction Works

The fare estimation workflow combines geographic information and configured pricing rules with available historical ride data.

1. The passenger selects pickup and destination locations.
2. The application obtains their geographic coordinates.
3. The system estimates the trip distance.
4. The application calculates an approximate ETA.
5. The fare prediction component estimates the ride cost.
6. A predicted fare range and confidence indicator are displayed.
7. The estimated fare is stored with the booking.

A basic fare calculation can follow this formula:

**Estimated Fare = Base Fare + (Distance × Rate per Distance Unit)**

Additional adjustments may apply according to the implemented ride types and historical-data logic.

## 🌐 Internet and Mapping

OpenStreetMap tiles and geocoding services normally require an internet connection. Offline map functionality depends on the availability and configuration of a suitable tile database.

## ⚠️ Current Limitations

- No live traffic information is claimed.
- No live GPS driver dispatch is claimed.
- Distance and ETA values are estimates.
- Fare prediction depends on available historical data and configured fare rules.
- No real payment gateway is claimed.
- Demo credentials are not suitable for production use.

## 🔮 Future Improvements

- Road-routing integration for more accurate distances.
- Live traffic-aware ETA calculation.
- Real-time driver tracking.
- Secure registration and authentication.
- An evaluated machine-learning fare prediction model.
- Online payment integration.
- Ride history and digital receipts.
- Improved offline mapping support.
- Cloud deployment and automated testing.

## 🎯 Project Objective

My objective is to develop a practical ride-booking application that combines interactive maps, geographic calculations, estimated journey times, and data-driven fare prediction. Through this project, I aim to strengthen my skills in Python development, GUI design, mapping integration, database management, and intelligent estimation systems.

## 👨‍💻 Project Information

- **Project Name:** Pakistan Ride
- **Category:** Python Desktop Application
- **Primary Language:** Python
- **Interface:** Tkinter
- **Mapping:** TkinterMapView and OpenStreetMap
- **Core Focus:** Smart Mapping, Ride Booking, and AI-Style Fare Prediction
- **Platform:** Windows

---

*Pakistan Ride is a learning and demonstration project. Estimated fares and journey times are not guaranteed real-world prices or travel times.*
