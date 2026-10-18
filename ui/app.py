# Omni's UI Application
import httpx
import config
from services.weather import fetch_weather_data  # Clean import from your service folder

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import Footer, Header, Input, Markdown, OptionList, Static
from textual.widgets.option_list import Option
from textual.worker import Worker, WorkerState

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

from services.llm import generate_chat_response

# Available slash tags / commands mapped to their descriptions
AVAILABLE_COMMANDS = {
    "/weather": "Inject live weather metrics into system context",
    "/clear": "Clear conversation history and reset screen",
    "/compact": "Compact conversation history context",
}


class OmniChatApp(App):
    """Sleek Claude-Code inspired TUI with Slash Command Autocomplete."""

    CSS = """
    Screen {
        background: #1e1e1e;
        color: #d4d4d4;
    }

    /* Top Welcome Banner */
    #welcome-banner {
        height: 12;
        margin: 1 2 0 2;
        border: round #d97706;
        background: #262626;
    }

    #banner-left {
        width: 1fr;
        padding: 1 2;
        align: center middle;
        content-align: center middle;
    }

    #banner-right {
        width: 1fr;
        border-left: solid #404040;
        padding: 1 2;
    }

    /* Chat Scroll Area */
    VerticalScroll {
        height: 1fr;
        padding: 1 2;
    }

    .message {
        margin: 1 0;
        padding: 1 2;
        border: round #404040;
        background: #262626;
    }

    .user-msg {
        border: round #3b82f6;
        border-title-color: #60a5fa;
    }

    .ai-msg {
        border: round #10b981;
        border-title-color: #34d399;
    }

    .system-msg {
        border: round #f59e0b;
        color: #a3a3a3;
        text-style: italic;
    }

    /* Input & Autocomplete Area */
    #input-container {
        dock: bottom;
        height: auto;
        margin: 0 2 1 2;
    }

    #autocomplete-popup {
        height: 6;
        background: #262626;
        border: round #3b82f6;
        display: none;
        margin-bottom: 1;
    }

    Input {
        border: round #d97706;
        background: #262626;
        padding: 0 1;
    }
    """

    BINDINGS = [
        ("c", "quit", "Quit"),
        ("ctrl+l", "clear_chat", "Clear Screen"),
    ]

    def on_mount(self) -> None:
        self.conversation_history = []
        self.query_one("#user-input", Input).focus()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        # Top Banner matching Claude Code layout
        with Container(id="welcome-banner"):
            with Horizontal():
                with Vertical(id="banner-left"):
                    yield Static(
                        "[bold #d97706]Omni TUI v1.0.0[bold]\n\n"
                        "    █▀█ █▀▄▀█ █▄ █ █\n"
                        "    █▄█ █ ▀ █ █ ▀█ █\n\n"
                        "[dim]Local & Cloud AI Terminal[dim]"
                    )
                with Vertical(id="banner-right"):
                    yield Static(
                        "[bold #f59e0b]Available Slash Commands[bold]\n"
                        "[dim]Type [bold #60a5fa]/[bold] in prompt below to open menu:[/dim]\n\n"
                        "• [bold]/weather[bold] - Live weather contextual prompt\n"
                        "• [bold]/clear[bold] - Clear screen & chat memory\n"
                        "• [bold]/compact[bold] - Summarize context"
                    )

        # Chat message viewport
        yield VerticalScroll(id="chat-scroll")

        # Bottom Input + Floating Autocomplete Menu
        with Vertical(id="input-container"):
            yield OptionList(id="autocomplete-popup")
            yield Input(
                placeholder="> Type a message or / for commands...",
                id="user-input",
            )

        yield Footer()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Triggers the slash popup list whenever input starts with '/' or '@'."""
        text = event.value
        popup = self.query_one("#autocomplete-popup", OptionList)

        if text.startswith("/") or text.startswith("@"):
            popup.clear_options()
            filter_str = text.lower()

            # Filter command suggestions
            for cmd, desc in AVAILABLE_COMMANDS.items():
                if cmd.startswith(filter_str) or filter_str in ("/", "@"):
                    popup.add_option(Option(f"{cmd:<15} [dim]{desc}[/dim]", id=cmd))

            if popup.option_count > 0:
                popup.styles.display = "block"
            else:
                popup.styles.display = "none"
        else:
            popup.styles.display = "none"

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Applies the selected command from the popup menu into the Input box."""
        selected_cmd = str(event.option.id)
        input_widget = self.query_one("#user-input", Input)

        if selected_cmd == "/clear":
            self.action_clear_chat()
            input_widget.value = ""
        else:
            input_widget.value = f"{selected_cmd} "
            input_widget.cursor_position = len(input_widget.value)

        self.query_one("#autocomplete-popup", OptionList).styles.display = "none"
        input_widget.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        user_text = event.value.strip()
        if not user_text:
            return

        # Hide popup menu
        self.query_one("#autocomplete-popup", OptionList).styles.display = "none"

        input_widget = self.query_one("#user-input", Input)
        input_widget.value = ""

        # Handle local commands
        if user_text == "/clear":
            self.action_clear_chat()
            return

        # Remove the welcome banner permanently on the first submitted prompt
        try:
            banner = self.query_one("#welcome-banner", Container)
            banner.remove()
        except Exception:
            pass

        scroll = self.query_one("#chat-scroll", VerticalScroll)

        # Render User Message Box
        user_box = Static(user_text, classes="message user-msg")
        user_box.border_title = " You "
        scroll.mount(user_box)

        # Store in memory
        self.conversation_history.append({"role": "user", "content": user_text})

        # Render Status Box
        thinking_box = Static(
            "⚡ Processing request...", classes="message system-msg", id="thinking"
        )
        thinking_box.border_title = " Omni Status "
        scroll.mount(thinking_box)
        scroll.scroll_end(animate=False)

        # Dispatch async query
        history_snapshot = list(self.conversation_history)
        self.run_worker(
            lambda: generate_chat_response(history_snapshot),
            exclusive=False,
            thread=True,
        )

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.state == WorkerState.SUCCESS:
            scroll = self.query_one("#chat-scroll", VerticalScroll)

            try:
                self.query_one("#thinking", Static).remove()
            except Exception:
                pass

            ai_response = event.worker.result
            self.conversation_history.append({"role": "assistant", "content": ai_response})

            ai_box = Markdown(ai_response, classes="message ai-msg")
            ai_box.border_title = " Omni AI "
            scroll.mount(ai_box)
            scroll.scroll_end(animate=True)

        elif event.state == WorkerState.ERROR:
            scroll = self.query_one("#chat-scroll", VerticalScroll)
            try:
                self.query_one("#thinking", Static).remove()
            except Exception:
                pass

            err_box = Static(
                f"Error: {event.worker.error}", classes="message system-msg"
            )
            err_box.border_title = " System Error "
            scroll.mount(err_box)
            scroll.scroll_end(animate=True)

    def action_clear_chat(self) -> None:
        self.conversation_history.clear()
        scroll = self.query_one("#chat-scroll, VerticalScroll")
        # If the welcome banner was removed, clearing/resetting can optionally restore it, or just clear messages:
        scroll.query("*").remove()
