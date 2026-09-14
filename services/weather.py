import httpx
import config

def fetch_weather_data() -> dict:
    """Fetches current weather data from the configured API URL."""
    with httpx.Client() as client:
        response = client.get(config.WEATHER_API_URL)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    # Moving the import here breaks the circular loop during initial load
    from ui.app import WeatherApp

    weatherapplet = WeatherApp()
    weatherapplet.run()
