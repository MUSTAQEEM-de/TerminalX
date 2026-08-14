import os

from dotenv import load_dotenv
from groq import Groq
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from safety import check_command
from executor import execute_command


# ==============================
# Setup
# ==============================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set in .env")

client = Groq(api_key=api_key)

console = Console()


# ==============================
# AI
# ==============================

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

User: disk space batao
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


# ==============================
# Welcome Screen
# ==============================

def show_welcome():

    console.clear()

    logo = Text()
    logo.append("██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗██████╗ ███████╗██████╗ ████████╗\n",
                style="bold green")
    logo.append("██║     ██║████╗  ██║██║   ██║╚██╗██╔╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝\n",
                style="bold green")
    logo.append("██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝ ██████╔╝█████╗  ██████╔╝   ██║   \n",
                style="bold cyan")
    logo.append("██║     ██║██║╚██╗██║██║   ██║ ██╔██╗ ██╔═══╝ ██╔══╝  ██╔══██╗   ██║   \n",
                style="bold cyan")
    logo.append("███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗██║     ███████╗██║  ██║   ██║   \n",
                style="bold blue")
    logo.append("╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝",
                style="bold blue")

    console.print(
        Panel(
            logo,
            title="[bold green]LinuXpert[/bold green] — [white]AI Linux Assistant[/white]",
            border_style="cyan",
            padding=(1, 2)
        )
    )

    console.print()

    info = Table.grid(padding=(0, 2))

    info.add_row(
        "[bold green]✦ Natural Language[/bold green]",
        "[white]English • Hindi • Hinglish[/white]"
    )

    info.add_row(
        "[bold cyan]⚙ AI Powered[/bold cyan]",
        "[white]Groq + Llama[/white]"
    )

    info.add_row(
        "[bold yellow]🛡 Safety[/bold yellow]",
        "[white]Dangerous commands require confirmation[/white]"
    )

    info.add_row(
        "[bold magenta]⚡ Execution[/bold magenta]",
        "[white]Commands execute directly in Ubuntu[/white]"
    )

    console.print(
        Panel(
            info,
            title="[bold]SYSTEM[/bold]",
            border_style="green"
        )
    )

    console.print()

    examples = Table.grid(padding=(0, 2))

    examples.add_row(
        "[green]file dikha[/green]",
        "[cyan]→[/cyan]",
        "[white]ls[/white]"
    )

    examples.add_row(
        "[green]xyz file bana[/green]",
        "[cyan]→[/cyan]",
        "[white]touch xyz[/white]"
    )

    examples.add_row(
        "[green]disk space batao[/green]",
        "[cyan]→[/cyan]",
        "[white]df -h[/white]"
    )

    examples.add_row(
        "[green]internet check karo[/green]",
        "[cyan]→[/cyan]",
        "[white]ping -c 4 google.com[/white]"
    )

    console.print(
        Panel(
            examples,
            title="[bold yellow]EXAMPLES[/bold yellow]",
            border_style="blue"
        )
    )

    console.print()

    console.print(
        "[dim]Type [bold red]exit[/bold red] to quit[/dim]"
    )

    console.print()


# ==============================
# Command Processing
# ==============================

def process_command(user_input):

    # Direct Linux command mode
    if user_input.startswith("!"):
        command = user_input[1:].strip()

        if not command:
            console.print(
                "[bold red]✗ Please enter a Linux command.[/bold red]"
            )
            return

    else:
        # AI mode
        try:
            with console.status(
                "[bold cyan]LinuXpert is thinking...[/bold cyan]",
                spinner="dots"
            ):
                command = ask_ai(user_input)

        except Exception as error:
            console.print(
                Panel(
                    str(error),
                    title="[bold red]AI Error[/bold red]",
                    border_style="red"
                )
            )
            return

    # AI generated command
    console.print(
        Panel(
            f"[bold cyan]{command}[/bold cyan]",
            title="[bold]Linux Command[/bold]",
            border_style="cyan"
        )
    )

    # Safety
    safety = check_command(command)

    if safety["safe"]:

        console.print(
            "[bold green]✓ Safety:[/bold green] "
            "[green]SAFE[/green]"
        )

        console.print(
            "[bold yellow]⚡ Executing...[/bold yellow]\n"
        )

        execute_command(command)

    else:

        console.print(
            "[bold yellow]⚠ Safety:[/bold yellow] "
            "[yellow]Confirmation required[/yellow]"
        )

        console.print(
            f"[dim]Reason: {safety['reason']}[/dim]"
        )

        console.print()

        confirmation = console.input(
            "[bold yellow]Execute this command? [y/N]: [/bold yellow]"
        )

        if confirmation.lower() == "y":

            console.print(
                "\n[bold yellow]⚡ Executing...[/bold yellow]\n"
            )

            execute_command(command)

        else:

            console.print(
                "[bold red]✗ Command cancelled.[/bold red]"
            )

    console.print()


# ==============================
# Main
# ==============================

def main():

    show_welcome()

    session = PromptSession(
        history=FileHistory(".linuXpert_history")
    )

    while True:

        try:

            user_input = session.prompt(
                "LinuXpert > "
            ).strip()

        except KeyboardInterrupt:
            console.print(
                "\n[dim]Press 'exit' to quit.[/dim]"
            )
            continue

        except EOFError:
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":

            console.print(
                "\n[bold green]LinuXpert session closed. 👋[/bold green]"
            )

            break

        process_command(user_input)


if __name__ == "__main__":
    main()