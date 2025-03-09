import logging
import yaml
import os

def setup_logging():
    logging.basicConfig(level=logging.INFO)

def handle_api_error(e):
    logging.error(f"API error: {e}")
    return {"error": str(e)}

def load_config():
    config_path = os.getenv("CONFIG_PATH", "config.yaml")
    with open(config_path, "r") as config_file:
        return yaml.safe_load(config_file)
