import requests

def get_geocoordinates(location):
    # Example using OpenStreetMap's Nominatim API
    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": location, "format": "json"},
    )
    data = response.json()
    if not data:
        raise ValueError(f"Location '{location}' not found.")

    lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
    return lat, lon
