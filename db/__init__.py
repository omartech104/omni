# Omni's Database Module
# Package Metadata
__version__ = "0.0.1"
__author__ = "Omar Mohammed"

# Up-importing (Exposing specific functions directly to the package level)
from .db import CalendarEvent, ChatMessage, Todo, get_session, init_db

# Defining what gets exported during 'from my_math_package import *'
__all__ = ["Todo", "CalendarEvent", "ChatMessage", "init_db", "get_session"]

# Package Initialization Code (Runs once when the package is imported)
print("omni.db has been initialized successfully!")
