# Omni's Configuration File
import os
from pathlib import Path

# Base directory paths
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db" / "omni.db"

# API Keys & Endpoints
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# LLM Configuration (Switch between OpenRouter or Local)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter")  # "openrouter" or "local"
LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://localhost:11434/v1")
LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL", "llama3")

# Default User Settings
DEFAULT_CITY = "Cairo"
DEFAULT_UNITS = "celsius"  # "celsius" or "imperial"

# API URLs
WEATHER_API_URL = f"https://api.openweathermap.org/data/2.5/weather?q={DEFAULT_CITY}&units={DEFAULT_UNITS}&appid={WEATHER_API_KEY}"
