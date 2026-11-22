import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Load existing memory
def load_memory():
    with open("memory.json", "r") as file:
        return json.load(file)


# Save information to memory
def save_memory(key: str, value: str) -> str:
    memory = load_memory()
    memory[key] = value

    with open("memory.json", "w") as file:
        json.dump(memory, file, indent=4)

    return "Information saved successfully."


chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config={
        "tools": [save_memory],
         "system_instruction": (
    "You are an AI Agent with persistent memory. "
    "Whenever the user shares personal information, "
    "you MUST call the save_memory tool to store it. "
    "For example, if the user says their name is Abhi, "
    "save it with key='name' and value='Abhi'."
)
    }
)

while True:
    question = input("You: ")

    if question.lower() == "exit":
        break

    try:
        memory = load_memory()

        prompt = f"""
        Saved user memory: {memory}

        User message: {question}

        Use saved memory when answering.
        """

        response = chat.send_message(prompt)

        print("Agent:", response.text)

    except Exception as e:
        print("Agent Error:", e)
