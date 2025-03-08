from ai_suggestions import get_ai_suggestions
from weather import get_open_meteo_weather
from locations import get_city_info
import logging

logging.basicConfig(level=logging.INFO)

def travel_info(city):
    next_days_from_curr_date = 2
    weather = get_open_meteo_weather(city, next_days_from_curr_date)
    city_info = get_city_info(city)
    ai_suggestions = get_ai_suggestions(f"Best travel recommendations for {city}")

    response = {
        "city": city,
        "weather": weather,
        "city_info": city_info,
        "ai_suggestions": ai_suggestions
    }
    return response

if __name__ == "__main__":
    try:
        city = "kolkata"
        info = travel_info(city)
        print(info)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
