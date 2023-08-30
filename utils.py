# utils.py

# Define a small database of city coordinates
city_coordinates = {
    'new york': (40.7128, -74.0060),
    'london': (51.5074, -0.1278),
    'tokyo': (35.6895, 139.6917),
    'paris': (48.8566, 2.3522),
    'sydney': (-33.8688, 151.2093),
    'los angeles': (34.0522, -118.2437)
}

def get_coordinates(city_name):
    """
    Given a city name, return its latitude and longitude as a tuple.
    If the city is not found, return None.
    """
    return city_coordinates.get(city_name.lower())

