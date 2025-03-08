from ai_suggestions import get_ai_suggestions
from weather import get_open_meteo_weather
from locations import get_city_info
import logging

logging.basicConfig(level=logging.INFO)

def travel_info(city):
    next_days_from_curr_date = 2
    weather = get_open_meteo_weather(city, next_days_from_curr_date)
    city_info = get_city_info(city)
    ai_suggestions = get_ai_suggestions(f"""Best travel recommendations for {city}. 
                                        Provide the output in a structured format, coloured bullets.""")

    response = {
        "city": city,
        "weather": weather,
        "city_info": city_info,
        "ai_suggestions": ai_suggestions
    }
    return response

def print_colored_suggestions(suggestions):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "reset": "\033[0m"
    }
    for suggestion in suggestions.split('\n'):
        color = colors.get("blue")  # Default color
        if "red" in suggestion.lower():
            color = colors.get("red")
        elif "green" in suggestion.lower():
            color = colors.get("green")
        elif "yellow" in suggestion.lower():
            color = colors.get("yellow")
        elif "magenta" in suggestion.lower():
            color = colors.get("magenta")
        elif "cyan" in suggestion.lower():
            color = colors.get("cyan")
        print(f"{color}{suggestion}{colors['reset']}")

if __name__ == "__main__":
    try:
        city = input("Enter the city name: ")
        info = travel_info(city)
        print(f"City: {info['city']}")
        print(f"Weather: {info['weather']}")
        print(f"City Info: {info['city_info']}")
        print("AI Suggestions:")
        print_colored_suggestions(info['ai_suggestions'])
    except Exception as e:
        logging.error(f"An error occurred: {e}")