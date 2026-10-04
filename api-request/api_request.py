import os

import requests

API_URL = os.getenv("WEATHERSTACK_URL", "https://api.weatherstack.com/current")
API_KEY = os.getenv("WEATHERSTACK_API_KEY")
CITY = os.getenv("WEATHER_CITY", "New York")


def fetch_data():
    print(f"Fetching weather data for {CITY} from the Weatherstack API ...")
    if not API_KEY:
        raise RuntimeError("WEATHERSTACK_API_KEY is not set")
    try:
        response = requests.get(API_URL, params={"access_key": API_KEY, "query": CITY}, timeout=30)
        response.raise_for_status()  # si 200 le programme continue, sinon on passe a l'exception
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise  # reaffiche l'erreur et arrete le programme
    data = response.json()
    # Weatherstack renvoie un code 200 meme en cas d'erreur (cle invalide, quota...)
    if "error" in data:
        raise RuntimeError(f"Weatherstack API error: {data['error'].get('info')}")
    print("API response received successfully")
    return data


def mock_fetch_data():
    return {'request': {'type': 'City', 'query': 'New York, United States of America', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'New York', 'country': 'United States of America', 'region': 'New York', 'lat': '40.714', 'lon': '-74.006', 'timezone_id': 'America/New_York', 'localtime': '2026-01-22 05:23', 'localtime_epoch': 1769059380, 'utc_offset': '-5.0'}, 'current': {'observation_time': '10:23 AM', 'temperature': 3, 'weather_code': 116, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0004_black_low_cloud.png'], 'weather_descriptions': ['Partly cloudy'], 'astro': {'sunrise': '07:14 AM', 'sunset': '05:02 PM', 'moonrise': '09:16 AM', 'moonset': '09:16 PM', 'moon_phase': 'Waxing Crescent', 'moon_illumination': 10}, 'air_quality': {'co': '309.85', 'no2': '18.05', 'o3': '57', 'so2': '9.15', 'pm2_5': '12.35', 'pm10': '12.45', 'us-epa-index': '1', 'gb-defra-index': '1'}, 'wind_speed': 21, 'wind_degree': 237, 'wind_dir': 'WSW', 'pressure': 1016, 'precip': 0, 'humidity': 54, 'cloudcover': 75, 'feelslike': -2, 'uv_index': 0, 'visibility': 16, 'is_day': 'no'}}
