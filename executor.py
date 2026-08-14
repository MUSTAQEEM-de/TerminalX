import subprocess
import shlex


# Interactive Linux programs
# These need direct terminal input/output.
INTERACTIVE_COMMANDS = {
    "nano",
    "vim",
    "vi",
    "less",
    "more",
    "top",
    "htop",
}


def show_exit_help(base_command):
    """
    Show useful instructions before opening an interactive program.
    """

    print()

    if base_command == "nano":
        print("💡 Nano shortcuts:")
        print("   Ctrl + X  → Exit")
        print("   Ctrl + O  → Save")
        print()

    elif base_command in {"vim", "vi"}:
        print("💡 Vim shortcuts:")
        print("   :q         → Exit")
        print("   :q!        → Exit without saving")
        print("   :wq        → Save & Exit")
        print()

    elif base_command in {"less", "more"}:
        print("💡 Press 'q' → Exit viewer")
        print()

    elif base_command == "top":
        print("💡 Press 'q' → Exit")
        print()

    elif base_command == "htop":
        print("💡 Press 'q' or F10 → Exit")
        print()


def execute_command(command):

    try:

        # Convert command into parts
        parts = shlex.split(command)

        if not parts:
            print("❌ Empty command")
            return

        # Get main command
        base_command = parts[0].split("/")[-1]

        # =====================================================
        # INTERACTIVE COMMANDS
        # =====================================================

        if base_command in INTERACTIVE_COMMANDS:

            print(f"\n🖥️ Opening {base_command}...\n")

            # Show instructions
            show_exit_help(base_command)

            # IMPORTANT:
            # Do NOT use capture_output=True here.
            # Interactive applications need direct terminal access.
            result = subprocess.run(
                ["bash", "-c", command]
            )

            if result.returncode == 0:
                print("\n✅ Returned to LinuXpert")

            else:
                print("\n❌ Command failed")

            return

        # =====================================================
        # NORMAL COMMANDS
        # =====================================================

        result = subprocess.run(
            ["bash", "-c", command],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:

            print("✅ Command executed successfully")

            # Show command output
            if result.stdout.strip():

                print("\nOutput:")
                print(result.stdout.strip())

        else:

            print("❌ Command failed")

            # Show error
            if result.stderr.strip():
                print(result.stderr.strip())

    except ValueError:

        print("❌ Invalid command syntax")

    except Exception as error:

        print("❌ Execution error:")
        print(error)