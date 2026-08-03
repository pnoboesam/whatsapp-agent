from app.config import BASE_DIR

def load_prompt(name):
    PROMPTS_DIR = BASE_DIR / "app" / "prompts"

    path = PROMPTS_DIR / f"{name}.txt"

    with open(path, "r", encoding="utf-8") as f:
        return f.read()
