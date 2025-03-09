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

