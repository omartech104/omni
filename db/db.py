# Omni's Database Module
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session
from config import DB_PATH

# 1. Todo Model (Task Manager)
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)
    due_date: Optional[str] = None  # Format: YYYY-MM-DD HH:MM
    priority: str = Field(default="medium")  # low, medium, high
    created_at: datetime = Field(default_factory=datetime.utcnow)

# 2. Calendar Event Model (Agenda / Calendar)
class CalendarEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    start_time: str  # Format: YYYY-MM-DD HH:MM
    end_time: Optional[str] = None
    is_synced: bool = Field(default=False)  # True if pulled from external iCal/Google

# 3. Chat Message Model (Chatbot History)
class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str  # "user", "assistant", or "system"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Database Engine & Setup Initialization
# Ensures the parent directory exists and creates the SQLite file
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}")

def init_db():
    """Creates the database tables if they don't already exist."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Context manager or helper to get a database session."""
    return Session(engine)
