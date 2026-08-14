import shlex


# Commands that are safe for our prototype
SAFE_COMMANDS = {
    "ls",
    "pwd",
    "whoami",
    "date",
    "hostname",
    "df",
    "free",
    "uname",
    "lsb_release",
    "ip",
    "ps",
    "cat",
    "find",
    "mkdir",
    "touch",
    "cp",
    "mv",
    "clear",
}


# Commands that can modify or damage the system
DANGEROUS_COMMANDS = {
    "rm",
    "sudo",
    "chmod",
    "chown",
    "kill",
    "pkill",
    "shutdown",
    "reboot",
    "apt",
    "apt-get",
    "dd",
    "mkfs",
}


def check_command(command):
    """
    Check whether a Linux command is safe to execute.
    """

    try:
        parts = shlex.split(command)

        if not parts:
            return {
                "safe": False,
                "requires_confirmation": False,
                "reason": "Empty command"
            }

        base_command = parts[0]

        # Remove path if command contains something like /bin/ls
        base_command = base_command.split("/")[-1]

        # Dangerous command
        if base_command in DANGEROUS_COMMANDS:
            return {
                "safe": False,
                "requires_confirmation": True,
                "reason": f"'{base_command}' can modify the system or delete data."
            }

        # Safe command
        if base_command in SAFE_COMMANDS:
            return {
                "safe": True,
                "requires_confirmation": False,
                "reason": "Command is allowed."
            }

        # Unknown command
        return {
            "safe": False,
            "requires_confirmation": True,
            "reason": "Unknown command. User confirmation required."
        }

    except ValueError:
        return {
            "safe": False,
            "requires_confirmation": True,
            "reason": "Invalid command syntax."
        }