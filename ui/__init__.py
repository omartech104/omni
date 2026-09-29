
"""UI package for Omni.

Provides the main Textual application class that displays the weather
dashboard (and eventually other UI components).
"""

# Re‑export the primary app class for convenient imports
from .app import WeatherApp

__all__ = ["WeatherApp"]
