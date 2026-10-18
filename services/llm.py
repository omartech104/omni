from openai import OpenAI
import config
from services.weather import fetch_weather_data

if getattr(config, "LLM_PROVIDER", "openrouter") == "local":
    client = OpenAI(
        base_url=config.LOCAL_LLM_URL,
        api_key="ollama"
    )
    MODEL_NAME = config.LOCAL_LLM_MODEL
else:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=config.OPENROUTER_API_KEY
    )
    MODEL_NAME = "openai/gpt-4o-mini"

# Registry supporting slash commands, tags, and fallback keywords
TRIGGER_REGISTRY = {
    "weather": {
        "tags": ["/weather", "@weather"],
        "keywords": ["weather", "temperature", "forecast", "rain", "outside", "degrees"],
        "fetcher": fetch_weather_data,
        "formatter": lambda data: (
            f"Live Weather Report for {data['name']}: {data['temp']}°C, {data['condition']}."
            if "error" not in data else f"Could not retrieve weather: {data['error']}"
        )
    },
}


def generate_chat_response(messages_history: list) -> str:
    """Generates a response from the LLM using conversation history and dynamic command triggers."""
    system_content = "You are Omni, a sleek and helpful terminal AI assistant."
    injected_contexts = []

    # Extract the latest user query from the message history list
    latest_user_query = ""
    for msg in reversed(messages_history):
        if msg.get("role") == "user":
            latest_user_query = msg.get("content", "").lower()
            break

    # Scan for matching tags or fallback keywords in the latest prompt
    for feature_name, config_data in TRIGGER_REGISTRY.items():
        has_tag = any(tag in latest_user_query for tag in config_data["tags"])
        has_keyword = any(kw in latest_user_query for kw in config_data["keywords"])

        if has_tag or has_keyword:
            try:
                raw_data = config_data["fetcher"]()
                formatted_context = config_data["formatter"](raw_data)
                injected_contexts.append(f"[Injected Context for {feature_name}]:\n{formatted_context}")
            except Exception as e:
                injected_contexts.append(f"[Injected Context for {feature_name}]: Error - {str(e)}")

    if injected_contexts:
        system_content += "\n\n" + "\n\n".join(injected_contexts)

    # Construct payload combining system instructions and the full chat history
    payload_messages = [{"role": "system", "content": system_content}] + messages_history

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=payload_messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI generation error: {str(e)}"


if __name__ == "__main__":
    from ui.app import OmniChatApp
    app = OmniChatApp()
    app.run()
