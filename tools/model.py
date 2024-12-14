def reset(thread):
    thread["model"] = "gtp-4o"
    thread["temperature"] = 0
    
def run(model: str, temperature: int, thread: dict):
    "Sets the llm model, gtp-4o or gpt-4o-mini, and temperature, 0 to 100."
    thread["model"] = model
    thread["temperature"] = temperature / 100
    return "success"
