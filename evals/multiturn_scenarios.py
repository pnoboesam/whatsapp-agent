from dotenv import load_dotenv

from app.agent.agent import chat

load_dotenv()

SCENARIO = [
    "I have keloids on my face and I'd like to book a consultation.",
    "They've been there for about a year and they're itchy.",
    "Yes, please help me book.",
    "My name is John Doe, my number is 0241234567, and I'm in East Legon.",
    "Yes, that's correct.",
]

def main():
    thread_id = "eval-multiturn-keliod-001"

    for i, message in enumerate(SCENARIO, start=1):
        print(f"\n{'=' * 60}")
        print(f"TURN {i}")
        print(f"{'=' * 60}")
        print(f"USER: {message}")

        response = chat(
            thread_id=thread_id,
            message=message,
        )

        print(f"AGENT: {response}")


if __name__ == "__main__":
    main()