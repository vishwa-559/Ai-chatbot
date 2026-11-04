import os
import ollama
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

client = ollama.Client(host=HOST)

history = [
    {"role": "system", "content": "You are a helpful assistant."}
]


def chat_loop():
    print(f"Chatting with {MODEL}. Type 'exit' to quit, 'clear' to reset.\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Bye!")
            break
        if user_input.lower() == "clear":
            del history[1:]
            print("History cleared.\n")
            continue

        history.append({"role": "user", "content": user_input})
        reply = ""
        print("Bot: ", end="", flush=True)

        try:
            for chunk in client.chat(model=MODEL, messages=history, stream=True):
                piece = chunk["message"]["content"]
                print(piece, end="", flush=True)
                reply += piece
        except ollama.ResponseError as e:
            print(f"\n[Ollama error] {e}")
            history.pop()
            continue
        except Exception as e:
            print(f"\n[Connection error] Is Ollama running? {e}")
            history.pop()
            continue

        print("\n")
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    chat_loop()