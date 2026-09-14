# Omni's UI Application
import httpx
import config
from services.weather import fetch_weather_data  # Clean import from your service folder

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Container

class WeatherApp(App):
    """A Textual app to display Omni Weather data."""

    CSS = """
    Container {
        layout: vertical;
        align: center middle;
        background: $boost;
        padding: 2;
    }
    Static {
        content-align: center middle;
        text-style: bold;
        color: $accent;
        border: solid $primary;
        padding: 1 2;
        margin: 1;
    }
    """

    BINDINGS = [("q", "quit", "Quit Application")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        # Fetching the live data
        try:
            data = fetch_weather_data()
            city = data.get("name", "Unknown City")
            temp_kelvin = data.get("main", {}).get("temp", 0)
            temp_celsius = round(temp_kelvin - 273.15, 1)
            condition = data.get("weather", [{}])[0].get("description", "N/A").title()

            display_text = f"🏙️  City: {city}\n\n🌡️  Temperature: {temp_celsius}°C\n\n🌤️  Condition: {condition}"
        except Exception as e:
            display_text = f"❌ Error fetching weather data:\n{str(e)}"

        yield Container(
            Static(display_text)
        )
        yield Footer()
