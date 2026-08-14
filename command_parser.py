import re


def parse_command(text):
    text = text.lower().strip()

    # =========================================================
    # FILE OPERATIONS
    # =========================================================

    # Create a file
    if text.startswith("create a file"):
        filename = text.replace("create a file", "", 1).strip()

        if filename:
            return f"touch {filename}"

        return "echo 'Please provide a file name'"

    if text.startswith("make a file"):
        filename = text.replace("make a file", "", 1).strip()

        if filename:
            return f"touch {filename}"

        return "echo 'Please provide a file name'"

    # Delete a file
    if text.startswith("delete file"):
        filename = text.replace("delete file", "", 1).strip()

        if filename:
            return f"rm -i {filename}"

        return "echo 'Please provide a file name'"

    if text.startswith("remove file"):
        filename = text.replace("remove file", "", 1).strip()

        if filename:
            return f"rm -i {filename}"

        return "echo 'Please provide a file name'"

    # Rename a file
    if text.startswith("rename file"):
        parts = text.replace("rename file", "", 1).strip().split()

        if len(parts) >= 3 and "to" in parts:
            index = parts.index("to")
            old_name = " ".join(parts[:index])
            new_name = " ".join(parts[index + 1:])

            return f"mv {old_name} {new_name}"

        return "echo 'Use: rename file old.txt to new.txt'"

    # Copy a file
    if text.startswith("copy file"):
        parts = text.replace("copy file", "", 1).strip().split()

        if len(parts) >= 3 and "to" in parts:
            index = parts.index("to")
            source = " ".join(parts[:index])
            destination = " ".join(parts[index + 1:])

            return f"cp {source} {destination}"

        return "echo 'Use: copy file file.txt to folder/'"

    # Move a file
    if text.startswith("move file"):
        parts = text.replace("move file", "", 1).strip().split()

        if len(parts) >= 3 and "to" in parts:
            index = parts.index("to")
            source = " ".join(parts[:index])
            destination = " ".join(parts[index + 1:])

            return f"mv {source} {destination}"

        return "echo 'Use: move file file.txt to folder/'"

    # =========================================================
    # DIRECTORY / FOLDER OPERATIONS
    # =========================================================

    # Create folder
    if text.startswith("create a folder"):
        folder = text.replace("create a folder", "", 1).strip()

        if folder:
            return f"mkdir -p {folder}"

        return "echo 'Please provide a folder name'"

    if text.startswith("create folder"):
        folder = text.replace("create folder", "", 1).strip()

        if folder:
            return f"mkdir -p {folder}"

        return "echo 'Please provide a folder name'"

    # Delete folder
    if text.startswith("delete folder"):
        folder = text.replace("delete folder", "", 1).strip()

        if folder:
            return f"rm -ri {folder}"

        return "echo 'Please provide a folder name'"

    if text.startswith("remove folder"):
        folder = text.replace("remove folder", "", 1).strip()

        if folder:
            return f"rm -ri {folder}"

        return "echo 'Please provide a folder name'"

    # =========================================================
    # LIST / DIRECTORY
    # =========================================================

    if text in [
        "show files",
        "list files",
        "show all files",
        "what files are here"
    ]:
        return "ls"

    if text in [
        "show detailed files",
        "list detailed files",
        "show file details"
    ]:
        return "ls -lah"

    if text in [
        "show hidden files",
        "list hidden files"
    ]:
        return "ls -la"

    # Current directory
    if text in [
        "where am i",
        "current directory",
        "show current directory",
        "what directory am i in"
    ]:
        return "pwd"

    # =========================================================
    # NAVIGATION
    # =========================================================

    if text in ["go home", "go to home", "home directory"]:
        return "cd ~"

    if text in ["go back", "previous directory"]:
        return "cd .."

    if text in ["go to root", "root directory"]:
        return "cd /"

    # =========================================================
    # SYSTEM INFORMATION
    # =========================================================

    if text in [
        "show system information",
        "system information",
        "tell me about my system"
    ]:
        return "uname -a"

    if text in [
        "show linux version",
        "linux version",
        "what linux version am i using"
    ]:
        return "lsb_release -a"

    if text in [
        "show kernel version",
        "kernel version"
    ]:
        return "uname -r"

    if text in [
        "show hostname",
        "what is my hostname",
        "computer name"
    ]:
        return "hostname"

    # =========================================================
    # DISK / STORAGE
    # =========================================================

    if text in [
        "check disk space",
        "show disk space",
        "how much disk space is available",
        "disk usage"
    ]:
        return "df -h"

    if text in [
        "show folder size",
        "check folder size",
        "how big is this folder"
    ]:
        return "du -sh ."

    # =========================================================
    # MEMORY / CPU
    # =========================================================

    if text in [
        "check memory",
        "show memory",
        "memory usage",
        "how much ram am i using"
    ]:
        return "free -h"

    if text in [
        "show cpu",
        "cpu information",
        "check cpu"
    ]:
        return "lscpu"

    # =========================================================
    # PROCESSES
    # =========================================================

    if text in [
        "show running processes",
        "list processes",
        "show processes"
    ]:
        return "ps aux"

    if text in [
        "show top processes",
        "what is using cpu"
    ]:
        return "top -b -n 1 | head -20"

    # =========================================================
    # NETWORK
    # =========================================================

    if text in [
        "show ip",
        "show ip address",
        "what is my ip",
        "check ip"
    ]:
        return "ip addr"

    if text in [
        "check internet",
        "is internet working",
        "test internet"
    ]:
        return "ping -c 4 google.com"

    # =========================================================
    # DATE / TIME
    # =========================================================

    if text in [
        "what time is it",
        "show time",
        "current time"
    ]:
        return "date '+%H:%M:%S'"

    if text in [
        "what is today's date",
        "show date",
        "current date"
    ]:
        return "date '+%Y-%m-%d'"

    # =========================================================
    # USER INFORMATION
    # =========================================================

    if text in [
        "who am i",
        "show current user",
        "current user"
    ]:
        return "whoami"

    if text in [
        "show users",
        "list users"
    ]:
        return "cut -d: -f1 /etc/passwd"

    # =========================================================
    # FILE CONTENT
    # =========================================================

    if text.startswith("show content of"):
        filename = text.replace("show content of", "", 1).strip()

        if filename:
            return f"cat {filename}"

        return "echo 'Please provide a file name'"

    if text.startswith("read file"):
        filename = text.replace("read file", "", 1).strip()

        if filename:
            return f"cat {filename}"

        return "echo 'Please provide a file name'"

    # =========================================================
    # SEARCH
    # =========================================================

    if text.startswith("find file"):
        filename = text.replace("find file", "", 1).strip()

        if filename:
            return f"find . -name '{filename}'"

        return "echo 'Please provide a file name'"

    # =========================================================
    # PACKAGE MANAGEMENT
    # =========================================================

    if text.startswith("install"):
        package = text.replace("install", "", 1).strip()

        if package:
            return f"sudo apt install {package}"

        return "echo 'Please provide a package name'"

    if text.startswith("update packages"):
        return "sudo apt update"

    if text in [
        "upgrade packages",
        "update and upgrade packages"
    ]:
        return "sudo apt update && sudo apt upgrade"

    # =========================================================
    # GIT
    # =========================================================

    if text in ["git status", "show git status"]:
        return "git status"

    if text in ["initialize git", "create git repository"]:
        return "git init"

    # =========================================================
    # CLEAR TERMINAL
    # =========================================================

    if text in [
        "clear screen",
        "clear terminal",
        "clean terminal"
    ]:
        return "clear"

    # =========================================================
    # UNKNOWN COMMAND
    # =========================================================

    return "echo 'Sorry, I do not understand this command yet.'"