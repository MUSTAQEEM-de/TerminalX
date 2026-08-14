import os

from dotenv import load_dotenv
from groq import Groq
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

from safety import check_command
from executor import execute_command


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set in .env")

client = Groq(api_key=api_key)


def ask_ai(user_text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """
You are LinuXpert, an AI Linux command assistant.

Understand English, Hindi and Hinglish.

Convert the user's request into ONE Linux command.

Examples:

User: file dikha
Command: ls

User: files batao
Command: ls

User: mujhe files dekhni hai
Command: ls

User: xyz naam ki file bana
Command: touch xyz

User: xyz file create karo
Command: touch xyz

User: folder bana test
Command: mkdir test

User: mai kaha hu
Command: pwd

User: current location batao
Command: pwd

User: disk space kitni hai
Command: df -h

User: memory check karo
Command: free -h

User: internet check karo
Command: ping -c 4 google.com

Return ONLY the Linux command.
Do not explain anything.
"""
            },
            {
                "role": "user",
                "content": user_text
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


def process_command(user_input):

    # Direct Linux command mode
    if user_input.startswith("!"):
        command = user_input[1:].strip()

        if not command:
            print("Please enter a Linux command.")
            return

    else:
        # AI mode
        command = ask_ai(user_input)

    print(f"\nLinux Command: {command}")

    # Safety check
    safety = check_command(command)

    if safety["safe"]:
        print("Safety: SAFE")
        print("Executing...\n")

        execute_command(command)

    else:
        print("Safety: ⚠️ Confirmation required")
        print(f"Reason: {safety['reason']}")

        confirmation = input("Execute this command? [y/N]: ")

        if confirmation.lower() == "y":
            print("\nExecuting...\n")
            execute_command(command)
        else:
            print("❌ Command cancelled.")

    print()


def main():

    print("=================================")
    print("          LinuXpert")
    print("=================================")
    print("Natural language Linux assistant")
    print()
    print("Examples:")
    print("  file dikha")
    print("  xyz file bana")
    print("  disk space batao")
    print()
    print("Direct Linux command:")
    print("  !ls")
    print("  !pwd")
    print("exit = quit")
    print()

    # Persistent command history
    session = PromptSession(
        history=FileHistory(".linuXpert_history")
    )

    while True:

        try:
            user_input = session.prompt("LinuXpert > ").strip()

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
            continue

        except EOFError:
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        process_command(user_input)


if __name__ == "__main__":
    main()