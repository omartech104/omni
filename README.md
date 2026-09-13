Here is the updated README tailored to explicitly highlight how **`config.py`** manages your environment variables, application paths, and API settings:

---

# Omni 🚀

Omni is a modern, blazing-fast, and keyboard-driven terminal dashboard built in Python. It brings together your essential daily tools into a single interface—featuring real-time weather tracking, a task manager, a calendar agenda, and an AI-powered chatbot supporting both OpenRouter and local LLMs.

---

## ✨ Features

* **🤖 AI Chatbot:** Stream responses from cloud models via OpenRouter or connect directly to local LLMs (e.g., Ollama).
* **⛅ Weather Tracking:** Get instant, clean forecasts right in your terminal.
* **📝 Todo List:** Manage tasks with local persistence and zero bloat.
* **📅 Calendar Sync:** View and track your upcoming schedule and agenda.
* **⌨️ Global Shortcuts:** Summon or control Omni from anywhere in your operating system.
* **⚡ Modern TUI:** Built using **Textual** and **Rich** for a sleek, developer-friendly aesthetic.

---

## 📁 Project Architecture

```text
omni/
├── main.py              # Entry point to bootstrap the app
├── config.py            # Centralized configuration (loads .env and app paths)
├── services/            # External APIs and backend logic
│   ├── __init__.py
│   ├── weather.py       # Weather API client
│   ├── llm.py           # OpenRouter & Local LLM wrapper
│   └── calendar_sync.py # Calendar data handling
├── db/                  # Local data persistence
│   ├── __init__.py
│   └── database.py      # SQLite / SQLModel storage for todos
├── shortcuts/           # Hotkey listener management
│   ├── __init__.py
│   └── hotkeys.py       # Global shortcut bindings
└── ui/                  # User Interface (TUI framework)
    ├── __init__.py
    └── app.py           # Main interface layout and event loops
```

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **TUI Framework:** [Textual](https://github.com/Textualize/textual) & [Rich](https://github.com/Textualize/rich)
* **Networking:** [Httpx](https://www.python-httpx.org/) & OpenAI Python SDK (for OpenRouter)
* **Database:** [SQLModel](https://sqlmodel.tiangolo.com/) (SQLite)
* **Hotkeys:** `keyboard` / `pynput`

---

## ⚙️ Installation & Setup

1. **Clone or download the repository:**
```bash
cd omni
```


2. **Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```


3. **Install dependencies:**
```bash
pip install textual rich httpx openai sqlmodel python-dotenv keyboard
```


4. **Configure `config.py` via `.env`:**
Create a `.env` file in the root directory. **`config.py`** reads these variables to configure your keys and endpoints globally across all services:
```env
# API Keys & Endpoints
OPENROUTER_API_KEY=your_openrouter_api_key_here
WEATHER_API_KEY=your_weather_api_key_here

# Optional: Local LLM integration (e.g., Ollama/LM Studio)
LOCAL_LLM_URL=http://localhost:11434/v1
LOCAL_LLM_MODEL=llama3

# App Preferences
DEFAULT_CITY=YourCityName
```


5. **Run Omni:**
```bash
python main.py
```



---

## ⌨️ Usage & Navigation

Omni is designed to be fully controlled via your keyboard:

* **Global Hotkey:** Trigger the application from anywhere using your configured system shortcut.
* **Navigation:** Use arrow keys or `Tab` to move between widgets (Chat, Weather, Todos, Calendar).
* **Quit:** Press `Ctrl+C` or map a custom quit key inside the TUI.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
