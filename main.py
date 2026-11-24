import os
from dotenv import load_dotenv
from agent import NutritionAgent

load_dotenv()


def main():
    provider = os.getenv("PROVIDER", "groq")
    agent = NutritionAgent(provider=provider)
    print(f"🥗 Nutrition Agent | provider={provider} | model={agent.model}")
    print("Type 'exit' to quit.\n")
    while True:
        text = input("you: ").strip()
        if text.lower() in ("exit", "quit", "خروج"):
            break
        if text:
            print(f"\n agent: {agent.chat(text)}\n")


if __name__ == "__main__":
    main()
