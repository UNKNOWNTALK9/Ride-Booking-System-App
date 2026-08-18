# Pakistan Ride v3.0

## Smart Map + AI Fare Prediction

New:
- Interactive TkinterMapView/OpenStreetMap map.
- Click map for pickup and destination.
- Search Pakistan starter locations and place them on the map.
- Distance estimate from map coordinates.
- ETA estimate by ride type.
- Local AI-style fare prediction using fare rules and historical completed rides.
- Prediction range and confidence.
- AI fare stored in bookings.

The map package supports interactive maps, markers, address lookup and offline tile databases. Map tiles/geocoding normally require internet access. No live traffic, live GPS dispatch, or real payment gateway is claimed.

## Windows
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py

## Demo accounts
Passenger: passenger / passenger123
Admin: admin / admin123
Driver: driver / driver123
