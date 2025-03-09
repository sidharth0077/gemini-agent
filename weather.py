import os
import requests
import logging
import pytz
from datetime import datetime
from utils import load_config

config = load_config()

API_KEY = os.getenv("OPENWEATHER_API_KEY", config["openweather_api_key"])

def get_city_coordinates(city_name, api_key):
    """Fetches the geographical coordinates of a city using OpenWeather Geocoding API."""
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    try:
        response = requests.get(geocoding_url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching city coordinates: {e}")
        return None, None

    if not data:
        logging.warning(f"No data found for city: {city_name}")
        return None, None

    return data[0]['lat'], data[0]['lon']

def get_open_meteo_weather(city, next_days_from_curr_date):
    """Fetches weather data from Open-Meteo."""
    base_url = "https://api.open-meteo.com/v1/forecast"
    latitude, longitude = get_city_coordinates(city, API_KEY)

    if isinstance(latitude, dict) and "error" in latitude:
        return latitude

    hourly_vars = "temperature_2m,relativehumidity_2m,precipitation_probability,windspeed_10m"
    daily_vars = "temperature_2m_max,temperature_2m_min,precipitation_sum"
    timezone = "auto"  # automatically detects timezone.
    units = "metric"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": hourly_vars,
        "daily": daily_vars,
        "timezone": timezone,
        "units": units
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
        return {"error": str(e)}

    date = weather_data["daily"]["time"][next_days_from_curr_date]
    day_min_temperature = weather_data["daily"]["temperature_2m_min"][next_days_from_curr_date]
    day_max_temperature = weather_data["daily"]["temperature_2m_max"][next_days_from_curr_date]
    return date, day_min_temperature, day_max_temperature

def get_local_time(city):
    """Fetches the local time and timezone information for a city."""
    latitude, longitude = get_city_coordinates(city, API_KEY)
    if latitude is None or longitude is None:
        return {"error": "Could not fetch coordinates for the city"}

    timezone_url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={config['timezonedb_api_key']}&format=json&by=position&lat={latitude}&lng={longitude}"
    try:
        response = requests.get(timezone_url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching timezone information: {e}")
        return {"error": str(e)}

    if data["status"] != "OK":
        logging.warning(f"Error in timezone data for city: {city}")
        return {"error": "Could not fetch timezone information"}

    local_time = datetime.now(pytz.timezone(data["zoneName"])).strftime('%Y-%m-%d %H:%M:%S')
    return {
        "local_time": local_time,
        "timezone": data["zoneName"]
    }




