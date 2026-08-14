LinuXpert

LinuXpert is an AI-powered Linux assistant that allows users to
control and use Linux through natural language instead of memorizing
Linux commands.

For example:

User:  xyz.txt file bana
AI:    touch xyz.txt

User:  file dikha
AI:    ls

User:  mai kaha hu
AI:    pwd

User:  xyz.txt file open kar
AI:    nano xyz.txt

The prototype uses Groq Cloud API + Llama to understand English,
Hindi, and Hinglish requests, converts them into Linux commands, checks
the command with a safety layer, and executes the command inside
Ubuntu/WSL.

✨ Features

🧠 Natural-language Linux commands

🌐 English, Hindi, and Hinglish support

🤖 Groq API with Llama model

🛡️ Safety checker before command execution

⚡ Automatic execution of approved commands

⚠️ Confirmation for risky or unknown commands

🖥️ Support for interactive commands such as nano, vim, less,
top, and htop

⌨️ Command history with ↑ and ↓

🔧 Direct Linux command mode using !

🎨 Rich terminal UI

🐧 Designed to run inside Ubuntu/WSL

🏗️ Architecture

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

📁 Project Structure

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

command_parser.py and the old main.py are not required for the
AI-based CLI because natural-language parsing is handled by the Llama
model.

🚀 Installation

Step 1 --- Install WSL

If you are using Windows, install WSL with Ubuntu.

Open PowerShell as Administrator:

wsl --install

Restart Windows if required.

Check WSL:

wsl --status

Check installed distributions:

wsl --list --verbose

You should have Ubuntu running with VERSION 2.

Step 2 --- Open Ubuntu

Start Ubuntu from Windows or run:

wsl

Check that Linux is working:

uname -a

Check the current user:

whoami

Step 3 --- Create the project

Inside Ubuntu:

mkdir -p ~/linux-ai-assistant
cd ~/linux-ai-assistant

Check your path:

pwd

Expected:

/home/<your-username>/linux-ai-assistant

Step 4 --- Create Python Virtual Environment

Install the required Python venv package if necessary:

sudo apt update
sudo apt install python3-venv -y

Create the virtual environment:

python3 -m venv venv

Activate it:

source venv/bin/activate

You should now see:

(venv) username@computer:~/linux-ai-assistant$

The (venv) means the project's Python virtual environment is active.

Step 5 --- Install Python Packages

With the virtual environment activated:

pip install groq python-dotenv prompt_toolkit rich

If you are also using the FastAPI prototype:

pip install "fastapi[standard]"

Verify:

pip show groq
pip show rich
pip show prompt_toolkit

🔑 Step 6 --- Create Groq API Key

Create a Groq API key from the Groq Console.

Do not put your API key directly inside Python code.

Create .env in the project root:

touch .env

Open it:

nano .env

Add:

GROQ_API_KEY=your_groq_api_key_here

Save the file.

Important

Never commit .env to GitHub.

🔒 Step 7 --- Create .gitignore

Create:

touch .gitignore

Add:

.env
venv/
__pycache__/
*.pyc
.linuXpert_history

This prevents secrets, the virtual environment, and local history from
being uploaded.

🧠 Step 8 --- Configure the AI Parser

ai_parser.py is responsible for:

Taking the user's natural-language request

Sending it to Groq

Asking the Llama model to generate one Linux command

Passing that command to the safety checker

Executing it if it is safe

Asking for confirmation if it is risky

Example:

LinuXpert > xyz.txt file bana

Linux Command: touch xyz.txt
Safety: SAFE
Executing...

✅ Command executed successfully

🛡️ Step 9 --- Safety Layer

The safety layer is implemented in:

safety.py

It classifies commands into:

Safe

Examples:

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

These can be automatically executed according to the current prototype
rules.

Risky / Unknown

Examples:

rm xyz
sudo apt install git
chmod ...
chown ...
kill ...
shutdown ...

These require user confirmation.

Example:

⚠️ This command requires confirmation.

Reason: 'rm' can modify the system or delete data.

Execute this command? [y/N]:

⚙️ Step 10 --- Command Executor

executor.py executes the generated Linux command.

Normal commands such as:

ls
pwd
touch xyz
mkdir test
df -h

are executed while their output is captured and displayed.

Interactive applications need direct terminal access.

Supported interactive commands include:

nano
vim
vi
less
more
top
htop

For example:

LinuXpert > xyz.txt file open kar

The AI can generate:

nano xyz.txt

LinuXpert displays help before opening the editor:

💡 Nano shortcuts:
   Ctrl + X  → Exit
   Ctrl + O  → Save

After leaving Nano:

✅ Returned to LinuXpert

▶️ Step 11 --- Run LinuXpert

Make sure you are inside the project:

cd ~/linux-ai-assistant

Activate the environment:

source venv/bin/activate

Run:

python3 ai_parser.py

You should see the LinuXpert terminal interface.

💬 Step 12 --- Test Natural Language

Try these commands:

Show files

file dikha

Expected:

ls

Create a file

xyz.txt ki file bana

Expected:

touch xyz.txt

Create a folder

test naam ka folder bana

Expected:

mkdir test

Current location

mai kaha hu

Expected:

pwd

Disk space

disk space batao

Expected:

df -h

Memory

memory check karo

Expected:

free -h

Internet

internet check karo

Expected:

ping -c 4 google.com

🖥️ Step 13 --- Interactive Commands

LinuXpert can also understand requests for interactive Linux
applications.

Example:

LinuXpert > xyz.txt file open kar

Possible AI result:

nano xyz.txt

After confirmation, Nano opens directly.

Nano

Ctrl + X  → Exit
Ctrl + O  → Save

Vim

:q       → Exit
:q!      → Exit without saving
:wq      → Save and exit

Less / More

q → Exit

Top

q → Exit

⌨️ Step 14 --- Command History

LinuXpert uses prompt_toolkit to provide command history.

Use:

↑

to get the previous command.

Use:

↓

to move forward through command history.

History is stored locally in:

.linuXpert_history

This file is ignored by Git.

🔧 Step 15 --- Direct Linux Command Mode

You can also run a Linux command directly by prefixing it with !.

Example:

LinuXpert > !ls

This sends:

ls

directly to the executor.

Another example:

LinuXpert > !pwd

The safety checker is still applied, so direct mode does not bypass the
safety layer.

🚪 Step 16 --- Exit LinuXpert

Type:

exit

Example:

LinuXpert > exit

The application closes.

🧪 Example Complete Session

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

Create a file:

LinuXpert > abc.txt file bana

Linux Command: touch abc.txt
Safety: SAFE
Executing...

✅ Command executed successfully

Open the file:

LinuXpert > abc.txt file open kar

Linux Command: nano abc.txt

⚠️ Safety: Confirmation required

Execute this command? [y/N]: y

🖥️ Opening nano...

💡 Nano shortcuts:
   Ctrl + X → Exit
   Ctrl + O → Save

🔐 Security Notes

LinuXpert executes commands on the Linux system, so security is
important.

The current prototype:

Uses a command safety checker

Requires confirmation for risky/unknown commands

Does not automatically approve every unknown command

Keeps the Groq API key in .env

Does not commit secrets to GitHub

Important

Do not give LinuXpert unrestricted sudo access without adding stronger
validation.

Future versions should include:

Command allowlist / risk scoring

Shell operator validation (;, &&, ||, |, redirects)

Path restrictions

Better sudo handling

Destructive-command detection

User confirmation for filesystem changes

Audit logs

Sandboxed execution

🧰 Technologies Used

Technology       Purpose

Python           Core application
Ubuntu / WSL 2   Linux execution environment
Groq API         Cloud AI inference
Llama            Natural-language understanding
FastAPI          API/backend prototype
prompt_toolkit   Interactive terminal and command history
Rich             Styled terminal UI
python-dotenv    Environment variable management

🗺️ Development Roadmap

Current Prototype

Ubuntu/WSL setup

Python virtual environment

Groq API integration

Natural-language command generation

English/Hindi/Hinglish input

Safety checker

Command execution

Interactive commands

Command history

Styled terminal UI

Next

Complete FastAPI integration

Web-based terminal interface

Better command risk classification

Shell operator protection

Better error recovery

Command explanation mode

Command history database

User permission system

Local model support with Ollama

RAG-based Linux documentation

Voice input

Multi-user support

🎯 Project Goal

LinuXpert aims to make Linux easier for beginners and users who do not
remember complex Linux commands.

Instead of remembering:

mkdir projects
cd projects
touch app.py
chmod +x app.py

the user can communicate naturally:

projects naam ka folder bana

uske andar jao

app.py file bana

app.py ko executable banao

The AI translates the user's intent into Linux operations while the
safety layer controls what can actually be executed.

🤝 Contributing

Contributions are welcome.

Basic workflow:

git clone <your-repository-url>
cd linux-ai-assistant

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

Create your own .env:

GROQ_API_KEY=your_api_key

Run:

python3 ai_parser.py

⚠️ Disclaimer

LinuXpert executes commands on the user's Linux environment.

Always review and test commands before allowing potentially destructive
operations.

This project is currently a prototype and should not be treated as a
production-grade system administration tool.

📜 License



LinuXpert License

LinuXpert --- Simplifying Linux, one command at a time.
