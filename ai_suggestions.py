from google import genai
import logging
import os
from utils import load_config

config = load_config()

logging.basicConfig(level=logging.INFO)

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY", config["google_api_key"]))

def get_ai_suggestions(query):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=query
        )
        return response.text
    except Exception as e:
        logging.error(f"Error fetching AI suggestions: {e}")
        return {"error": str(e)}