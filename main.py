from command_parser import parse_command
from executor import execute_command


def main():
    print("=================================")
    print("      Linux AI Assistant")
    print("=================================")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Linux Assistant > ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if not user_input:
            continue

        command = parse_command(user_input)

        print(f"Command: {command}")

        execute_command(command)
        print()


if __name__ == "__main__":
    main()