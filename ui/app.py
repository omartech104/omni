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
        border: round $primary;
        padding: 1 2;
        margin: 1;
    }
    """

    BINDINGS = [("c", "quit", "Quit Application")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        try:
            data = fetch_weather_data()
            city = data.get("name", "Unknown City")
            temp_celsius = round(data.get("temp", 0.0), 1)

            # WMO code lookups are gone! Just grab the raw string description text directly
            condition = data.get("condition", "Unknown")

            if "error" in data:
                condition = f"Error: {data['error']}"

        except Exception as e:
            city = "Error"
            temp_celsius = 0.0
            condition = "Failed to load weather data"

        # 🎯 FIX: These lines must be shifted to the left out of the 'except' block!
        display_text = f"📍 {city}\n🌡️ {temp_celsius}°C\n✨ {condition}"

        yield Container(
            Static(display_text)
        )
        yield Footer()
