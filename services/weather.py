import urllib.parse
import httpx
import config

def fetch_weather_data() -> dict:
    """Fetches text weather data cleanly using the wttr.in engine."""
    target_city = config.DEFAULT_CITY

    try:
        # Encode the city name cleanly for transmission strings (e.g. "Cairo")
        safe_city = urllib.parse.quote(target_city)
        url = config.WEATHER_API_URL.format(city_name=safe_city)

        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            raw_data = response.json()

            # Extract wttr.in JSON dictionary indices cleanly
            current = raw_data["current_condition"][0]

            return {
                "name": target_city.title(),
                "temp": float(current["temp_C"]),
                "condition": current["weatherDesc"][0]["value"]
            }

    except Exception as e:
        return {"name": target_city, "temp": 0.0, "condition": "Error", "error": str(e)}

if __name__ == "__main__":
    import ui
    result = fetch_weather_data()
    print(result)
    weatherapplet = ui.WeatherApp()
    weatherapplet.run()
