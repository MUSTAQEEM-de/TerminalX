# LinuXpert

**LinuXpert** is an AI-powered Linux assistant that allows users to
control and use Linux through natural language instead of memorizing
Linux commands.

For example:

``` text
User:  xyz.txt file bana
AI:    touch xyz.txt

User:  file dikha
AI:    ls

User:  mai kaha hu
AI:    pwd

User:  xyz.txt file open kar
AI:    nano xyz.txt
```

The prototype uses **Groq Cloud API + Llama** to understand English,
Hindi, and Hinglish requests, converts them into Linux commands, checks
the command with a safety layer, and executes the command inside
Ubuntu/WSL.

------------------------------------------------------------------------

## ✨ Features

-   🧠 Natural-language Linux commands
-   🌐 English, Hindi, and Hinglish support
-   🤖 Groq API with Llama model
-   🛡️ Safety checker before command execution
-   ⚡ Automatic execution of approved commands
-   ⚠️ Confirmation for risky or unknown commands
-   🖥️ Support for interactive commands such as `nano`, `vim`, `less`,
    `top`, and `htop`
-   ⌨️ Command history with `↑` and `↓`
-   🔧 Direct Linux command mode using `!`
-   🎨 Rich terminal UI
-   🐧 Designed to run inside Ubuntu/WSL

------------------------------------------------------------------------

# 🏗️ Architecture

``` text
                    User
                     │
                     ▼
             ┌───────────────┐
             │   LinuXpert   │
             │  CLI Terminal │
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │   Groq API    │
             │  Llama Model  │
             └───────┬───────┘
                     │
                     ▼
              Linux Command
                     │
                     ▼
             ┌───────────────┐
             │ Safety Checker│
             └───────┬───────┘
                     │
              ┌──────┴──────┐
              │             │
            SAFE          RISKY
              │             │
              │       User Confirmation
              │             │
              └──────┬──────┘
                     ▼
              ┌─────────────┐
              │   Executor  │
              └──────┬──────┘
                     ▼
                Ubuntu / WSL
                     │
                     ▼
                  Output
```

------------------------------------------------------------------------

# 📁 Project Structure

``` text
linux-ai-assistant/
│
├── ai_parser.py          # Main AI-powered CLI
├── safety.py              # Command safety checker
├── executor.py            # Executes Linux commands
├── api.py                 # FastAPI backend/prototype
│
├── .env                   # Groq API key (DO NOT COMMIT)
├── .gitignore             # Files ignored by Git
├── .linuXpert_history     # Command history (generated automatically)
│
└── venv/                  # Python virtual environment
```

> `command_parser.py` and the old `main.py` are not required for the
> AI-based CLI because natural-language parsing is handled by the Llama
> model.

------------------------------------------------------------------------

# 🚀 Installation

## Step 1 --- Install WSL

If you are using Windows, install WSL with Ubuntu.

Open **PowerShell as Administrator**:

``` powershell
wsl --install
```

Restart Windows if required.

Check WSL:

``` powershell
wsl --status
```

Check installed distributions:

``` powershell
wsl --list --verbose
```

You should have Ubuntu running with **VERSION 2**.

------------------------------------------------------------------------

# Step 2 --- Open Ubuntu

Start Ubuntu from Windows or run:

``` powershell
wsl
```

Check that Linux is working:

``` bash
uname -a
```

Check the current user:

``` bash
whoami
```

------------------------------------------------------------------------

# Step 3 --- Create the project

Inside Ubuntu:

``` bash
mkdir -p ~/linux-ai-assistant
cd ~/linux-ai-assistant
```

Check your path:

``` bash
pwd
```

Expected:

``` text
/home/<your-username>/linux-ai-assistant
```

------------------------------------------------------------------------

# Step 4 --- Create Python Virtual Environment

Install the required Python venv package if necessary:

``` bash
sudo apt update
sudo apt install python3-venv -y
```

Create the virtual environment:

``` bash
python3 -m venv venv
```

Activate it:

``` bash
source venv/bin/activate
```

You should now see:

``` text
(venv) username@computer:~/linux-ai-assistant$
```

The `(venv)` means the project's Python virtual environment is active.

------------------------------------------------------------------------

# Step 5 --- Install Python Packages

With the virtual environment activated:

``` bash
pip install groq python-dotenv prompt_toolkit rich
```

If you are also using the FastAPI prototype:

``` bash
pip install "fastapi[standard]"
```

Verify:

``` bash
pip show groq
pip show rich
pip show prompt_toolkit
```

------------------------------------------------------------------------

# 🔑 Step 6 --- Create Groq API Key

Create a Groq API key from the Groq Console.

Do **not** put your API key directly inside Python code.

Create `.env` in the project root:

``` bash
touch .env
```

Open it:

``` bash
nano .env
```

Add:

``` env
GROQ_API_KEY=your_groq_api_key_here
```

Save the file.

### Important

Never commit `.env` to GitHub.

------------------------------------------------------------------------

# 🔒 Step 7 --- Create `.gitignore`

Create:

``` bash
touch .gitignore
```

Add:

``` gitignore
.env
venv/
__pycache__/
*.pyc
.linuXpert_history
```

This prevents secrets, the virtual environment, and local history from
being uploaded.

------------------------------------------------------------------------

# 🧠 Step 8 --- Configure the AI Parser

`ai_parser.py` is responsible for:

1.  Taking the user's natural-language request
2.  Sending it to Groq
3.  Asking the Llama model to generate one Linux command
4.  Passing that command to the safety checker
5.  Executing it if it is safe
6.  Asking for confirmation if it is risky

Example:

``` text
LinuXpert > xyz.txt file bana

Linux Command: touch xyz.txt
Safety: SAFE
Executing...

✅ Command executed successfully
```

------------------------------------------------------------------------

# 🛡️ Step 9 --- Safety Layer

The safety layer is implemented in:

``` text
safety.py
```

It classifies commands into:

### Safe

Examples:

``` bash
ls
pwd
whoami
date
hostname
df
free
mkdir
touch
cp
mv
cat
find
```

These can be automatically executed according to the current prototype
rules.

### Risky / Unknown

Examples:

``` bash
rm xyz
sudo apt install git
chmod ...
chown ...
kill ...
shutdown ...
```

These require user confirmation.

Example:

``` text
⚠️ This command requires confirmation.

Reason: 'rm' can modify the system or delete data.

Execute this command? [y/N]:
```

------------------------------------------------------------------------

# ⚙️ Step 10 --- Command Executor

`executor.py` executes the generated Linux command.

Normal commands such as:

``` bash
ls
pwd
touch xyz
mkdir test
df -h
```

are executed while their output is captured and displayed.

Interactive applications need direct terminal access.

Supported interactive commands include:

``` text
nano
vim
vi
less
more
top
htop
```

For example:

``` text
LinuXpert > xyz.txt file open kar
```

The AI can generate:

``` bash
nano xyz.txt
```

LinuXpert displays help before opening the editor:

``` text
💡 Nano shortcuts:
   Ctrl + X  → Exit
   Ctrl + O  → Save
```

After leaving Nano:

``` text
✅ Returned to LinuXpert
```

------------------------------------------------------------------------

# ▶️ Step 11 --- Run LinuXpert

Make sure you are inside the project:

``` bash
cd ~/linux-ai-assistant
```

Activate the environment:

``` bash
source venv/bin/activate
```

Run:

``` bash
python3 ai_parser.py
```

You should see the LinuXpert terminal interface.

------------------------------------------------------------------------

# 💬 Step 12 --- Test Natural Language

Try these commands:

### Show files

``` text
file dikha
```

Expected:

``` bash
ls
```

### Create a file

``` text
xyz.txt ki file bana
```

Expected:

``` bash
touch xyz.txt
```

### Create a folder

``` text
test naam ka folder bana
```

Expected:

``` bash
mkdir test
```

### Current location

``` text
mai kaha hu
```

Expected:

``` bash
pwd
```

### Disk space

``` text
disk space batao
```

Expected:

``` bash
df -h
```

### Memory

``` text
memory check karo
```

Expected:

``` bash
free -h
```

### Internet

``` text
internet check karo
```

Expected:

``` bash
ping -c 4 google.com
```

------------------------------------------------------------------------

# 🖥️ Step 13 --- Interactive Commands

LinuXpert can also understand requests for interactive Linux
applications.

Example:

``` text
LinuXpert > xyz.txt file open kar
```

Possible AI result:

``` bash
nano xyz.txt
```

After confirmation, Nano opens directly.

### Nano

``` text
Ctrl + X  → Exit
Ctrl + O  → Save
```

### Vim

``` text
:q       → Exit
:q!      → Exit without saving
:wq      → Save and exit
```

### Less / More

``` text
q → Exit
```

### Top

``` text
q → Exit
```

------------------------------------------------------------------------

# ⌨️ Step 14 --- Command History

LinuXpert uses `prompt_toolkit` to provide command history.

Use:

``` text
↑
```

to get the previous command.

Use:

``` text
↓
```

to move forward through command history.

History is stored locally in:

``` text
.linuXpert_history
```

This file is ignored by Git.

------------------------------------------------------------------------

# 🔧 Step 15 --- Direct Linux Command Mode

You can also run a Linux command directly by prefixing it with `!`.

Example:

``` text
LinuXpert > !ls
```

This sends:

``` bash
ls
```

directly to the executor.

Another example:

``` text
LinuXpert > !pwd
```

The safety checker is still applied, so direct mode does not bypass the
safety layer.

------------------------------------------------------------------------

# 🚪 Step 16 --- Exit LinuXpert

Type:

``` text
exit
```

Example:

``` text
LinuXpert > exit
```

The application closes.

------------------------------------------------------------------------

# 🧪 Example Complete Session

``` text
LinuXpert > file dikha

Linux Command: ls
Safety: SAFE
Executing...

✅ Command executed successfully

Output:
ai_parser.py
api.py
executor.py
safety.py
venv
```

Create a file:

``` text
LinuXpert > abc.txt file bana

Linux Command: touch abc.txt
Safety: SAFE
Executing...

✅ Command executed successfully
```

Open the file:

``` text
LinuXpert > abc.txt file open kar

Linux Command: nano abc.txt

⚠️ Safety: Confirmation required

Execute this command? [y/N]: y

🖥️ Opening nano...

💡 Nano shortcuts:
   Ctrl + X → Exit
   Ctrl + O → Save
```

------------------------------------------------------------------------

# 🔐 Security Notes

LinuXpert executes commands on the Linux system, so security is
important.

The current prototype:

-   Uses a command safety checker
-   Requires confirmation for risky/unknown commands
-   Does not automatically approve every unknown command
-   Keeps the Groq API key in `.env`
-   Does not commit secrets to GitHub

### Important

Do not give LinuXpert unrestricted `sudo` access without adding stronger
validation.

Future versions should include:

-   Command allowlist / risk scoring
-   Shell operator validation (`;`, `&&`, `||`, `|`, redirects)
-   Path restrictions
-   Better `sudo` handling
-   Destructive-command detection
-   User confirmation for filesystem changes
-   Audit logs
-   Sandboxed execution

------------------------------------------------------------------------

# 🧰 Technologies Used

  Technology       Purpose
  ---------------- ------------------------------------------
  Python           Core application
  Ubuntu / WSL 2   Linux execution environment
  Groq API         Cloud AI inference
  Llama            Natural-language understanding
  FastAPI          API/backend prototype
  prompt_toolkit   Interactive terminal and command history
  Rich             Styled terminal UI
  python-dotenv    Environment variable management

------------------------------------------------------------------------

# 🗺️ Development Roadmap

## Current Prototype

-   [x] Ubuntu/WSL setup
-   [x] Python virtual environment
-   [x] Groq API integration
-   [x] Natural-language command generation
-   [x] English/Hindi/Hinglish input
-   [x] Safety checker
-   [x] Command execution
-   [x] Interactive commands
-   [x] Command history
-   [x] Styled terminal UI

## Next

-   [ ] Complete FastAPI integration
-   [ ] Web-based terminal interface
-   [ ] Better command risk classification
-   [ ] Shell operator protection
-   [ ] Better error recovery
-   [ ] Command explanation mode
-   [ ] Command history database
-   [ ] User permission system
-   [ ] Local model support with Ollama
-   [ ] RAG-based Linux documentation
-   [ ] Voice input
-   [ ] Multi-user support

------------------------------------------------------------------------

# 🎯 Project Goal

LinuXpert aims to make Linux easier for beginners and users who do not
remember complex Linux commands.

Instead of remembering:

``` bash
mkdir projects
cd projects
touch app.py
chmod +x app.py
```

the user can communicate naturally:

``` text
projects naam ka folder bana

uske andar jao

app.py file bana

app.py ko executable banao
```

The AI translates the user's intent into Linux operations while the
safety layer controls what can actually be executed.

------------------------------------------------------------------------

# 🤝 Contributing

Contributions are welcome.

Basic workflow:

``` bash
git clone <your-repository-url>
cd linux-ai-assistant

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Create your own `.env`:

``` env
GROQ_API_KEY=your_api_key
```

Run:

``` bash
python3 ai_parser.py
```

------------------------------------------------------------------------

# ⚠️ Disclaimer

LinuXpert executes commands on the user's Linux environment.

Always review and test commands before allowing potentially destructive
operations.

This project is currently a prototype and should not be treated as a
production-grade system administration tool.

------------------------------------------------------------------------

## 📜 License

Add your preferred license here, for example:

``` text
MIT License
```

------------------------------------------------------------------------

**LinuXpert --- Simplifying Linux, one command at a time.**
