import requests
import logging

logging.basicConfig(level=logging.INFO)

def get_city_info(city):
    """Fetches summary information about a city from Wikipedia."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{city}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching city info: {e}")
        return {"error": str(e)}

    if "extract" not in data:
        logging.warning(f"No information available for given city: {city}")
        return {"error": "No information available for the city"}

    return {
        "title": data["title"],
        "description": data["extract"],
        "url": data["content_urls"]["desktop"]["page"]
    }

def get_tourist_attractions(city):
    """Fetches popular tourist attractions for a city from Wikipedia."""
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={city}%20tourist%20attractions&format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching tourist attractions: {e}")
        return {"error": str(e)}

    attractions = []
    for page in data.get("query", {}).get("search", []):
        attractions.append(page["title"])

    if not attractions:
        logging.warning(f"No tourist attractions found for city: {city}")
        return {"error": "No tourist attractions found"}

    return attractions