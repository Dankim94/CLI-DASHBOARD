import requests #library to get the requests from open-meteo API
import openmeteo_requests #library to answer the requests
import requests_cache 
from retry_requests import retry #library to retry requests
from datetime import datetime

def get_location_coordinates_json(city_name): # function which allow to have the coordinates from the city entered 
    """
    Fetch latitude and longitude for a given city using Open-Meteo's Geocoding API in JSON format.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search" #link to research on the OPENMETEO API 
    params = {
        "name": city_name,
        "count": 1,       # Limiter à 1 résultat
        "language": "en", # Langue de la réponse
        "format": "json"  # Format JSON
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()  # Erreur si HTTP != 200

        data = response.json()

        # Vérifier si on a des résultats
        if "results" not in data or not data["results"]: #Handling places which doesn't exists
            print(f"No location found for '{city_name}'.")
            return None

        # looking for the first result 
        location = data["results"][0]
        name = location["name"]
        country = location.get("country", "Unknown")
        lat = location["latitude"]
        lon = location["longitude"]

        print(f"Location: {name}, {country}")
        print(f"Latitude: {lat}, Longitude: {lon}")

        return lat, lon

    except requests.exceptions.RequestException as e: #Handling errors 
        print(f"Error fetching location: {e}")
        return None

def get_coordinates(city: str):
    """
    Get latitude and longitude for a city using Open-Meteo's free geocoding API.
    """
    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {"name": city, "count": 1}  # count=1 returns the best match
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if "results" not in data or len(data["results"]) == 0:
            raise ValueError(f"No coordinates found for city: {city}")

        result = data["results"][0]
        return result["latitude"], result["longitude"], result["name"], result.get("country", "")
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
        return None


def get_current_weather_by_city(city: str):
    """
    Fetch current weather for a given city name.
    """
    coords = get_coordinates(city)
    if not coords:
        return None

    lat, lon, city_name, country = coords

    try:
        # Cache requests for 1 hour
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

        openmeteo = openmeteo_requests.Client(session=retry_session)

        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        }

        responses = openmeteo.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
        response = responses[0]
        current = response.Current()

        return {
            "city": city_name,
            "country": country,
            "temperature": round(current.Variables(0).Value(),1),
            "wind_speed" : round(current.Variables(1).Value(),2),
            "winddirection": round(current.Variables(2).Value(),2),
            "weathercode": current.Variables(3).Value(),
            "time": datetime.now() # get the current time 
        }

    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None


if __name__ == "__main__":
    city = input("Entrer city name :")
    weather = get_current_weather_by_city(city)
    if weather:
        print(f"Weather in {weather['city']}, {weather['country']}:") # Getting city and country
        print(f"Temperature: {weather['temperature']}°C") # Temperature in Celsius
        print(f"Wind speed: {weather['wind_speed']} km/h") # Wind speed 
        print(f"Wind direction: {weather['winddirection']}°")# Direction of the wind 
        print(f"Weather code: {weather['weathercode']}") # Don't know 
        print(f"Time: {weather['time']}") # Meteo in current time 

