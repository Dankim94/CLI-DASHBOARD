# Install dependencies before running:
# pip install openmeteo-requests requests-cache retry-requests

import openmeteo_requests 
import requests_cache
from retry_requests import retry

def get_location_coordinates_flatbuffers(city_name):
    """
    Fetch latitude and longitude for a given city using Open-Meteo's Geocoding API in FlatBuffers format.
    """
    # Cache et retry pour éviter les appels répétés et gérer les erreurs réseau
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=3, backoff_factor=0.3)

    # Client Open-Meteo
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # URL et paramètres
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "flatbuffers"  # Format binaire optimisé
    }

    # Appel API
    responses = openmeteo.geocoding(url, params=params)

    if not responses:
        print(f"No location found for '{city_name}'.")
        return None

    # On prend le premier résultat
    location = responses[0]
    name = location.name()
    country = location.country()
    lat = location.latitude()
    lon = location.longitude()

    print(f"Location: {name}, {country}")
    print(f"Latitude: {lat}, Longitude: {lon}")

    return lat, lon

# Exemple d'utilisation
if __name__ == "__main__":
    city = input("Enter city name: ").strip()
    coords = get_location_coordinates_flatbuffers(city)
    if coords:
        print(f"Coordinates: {coords}")
