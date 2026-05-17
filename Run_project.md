Perfect.
We’ll start the RIGHT way:

# foundation first

Before agents/MCP/AI, we need:

* reproducible environment
* clean project structure
* vulnerable Spring Boot app
* working FastAPI backend
* proper dependency management

Otherwise the project becomes unstable later.

---

# STEP 1 — Development Environment Setup

Since you're on Windows:

# use WSL2 Ubuntu

---

# 1. Verify WSL2

Inside PowerShell:

```powershell id="uw5c7t"
wsl --status
```

You should see:

* Default Version: 2
* Ubuntu installed

---

# 2. Open Ubuntu WSL

All development should happen INSIDE WSL.

NOT:

```text id="1x2jlwm"
C:\Users\...
```

Use:

```text id="7g3jgi"
/home/<your-user>/
```

---

# 3. Install System Packages

Inside Ubuntu:

```bash id="pazld4"
sudo apt update

sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    unzip \
    build-essential \
    openjdk-21-jdk \
    maven
```

---

# 4. Verify Java + Maven

```bash id="8ms8ys"
java -version
mvn -version
```

---

# 5. Install uv (VERY IMPORTANT)

`uv` is MUCH better than:

* pip
* requirements.txt
* venv manually

Install:

```bash id="tw3w1w"
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then restart terminal.

Verify:

```bash id="c7hfeh"
uv --version
```

Official docs:

[uv package manager](https://docs.astral.sh/uv/?utm_source=chatgpt.com)

---

# 6. Install Node.js

Needed later for MCP ecosystem.

Install nvm:

```bash id="t9r6sa"
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

Restart terminal.

Then:

```bash id="h6twt5"
nvm install --lts
```

Verify:

```bash id="ffebdm"
node -v
npm -v
```

---

# 7. Install Docker Desktop (Windows)

Install:

[Docker Desktop](https://www.docker.com/products/docker-desktop/?utm_source=chatgpt.com)

VERY IMPORTANT:
Enable:

```text id="m6z7mf"
Use WSL2 backend
```

Then verify inside WSL:

```bash id="p6fxoq"
docker ps
```

---

# STEP 2 — Create Project Structure

Inside WSL:

```bash id="vnnmpp"
mkdir -p ~/projects
cd ~/projects
```

Create project:

```bash id="xwzkxb"
mkdir patchpilot-ai
cd patchpilot-ai
```

---

# STEP 3 — Initialize Python Project

Using uv:

```bash id="zshx0u"
uv init
```

This creates:

```text id="7yfz7f"
pyproject.toml
```

---

# STEP 4 — Create Virtual Environment

```bash id="9rvahq"
uv venv
```

Activate:

```bash id="i1m7jq"
source .venv/bin/activate
```

---

# STEP 5 — Install Core Dependencies

Install FastAPI + OpenAI SDK stack:

```bash id="vq1u5y"
uv add \
    fastapi \
    uvicorn \
    pydantic \
    openai \
    openai-agents \
    python-dotenv \
    structlog \
    httpx \
    gitpython
```

---
Installing Docker on WSL 2 with Ubuntu 22.04
0_prerequisites.md
Installing Docker on WSL 2 with Ubuntu 22.04
Instalando Docker em um WSL 2 com Ubuntu 22.04

Prerequisites
Before start the installation process, make sure you meet the following prerequisites:

A Windows 10 operating system with WSL 2 support.
WSL 2 enabled.
Ubuntu 22.04 installed on WSL 2.
1_step1.md
Step 1: Update the system
Before installing Docker, it is a good practice to ensure that all system packages are up to date. Open the Ubuntu terminal in WSL 2 and run the following command:

sudo apt update && sudo apt upgrade -y
2_step2.md
Step 2: Install dependencies
Install the required dependencies for Docker:

sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
3_step3.md
Step 3: Add Docker GPG Key
Add the official Docker GPG key:

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
4_step4.md
Step 4: Add the Docker Repository
Add the Docker repository to the system:

echo "deb [signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
5_step5.md
Step 5: Install Docker Engine
Update repositories and install Docker Engine:

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
6_step6.md
Step 6: Add you user to Docker Group
Add your user to the Docker group to avoid the need to use sudo on every Docker command:

sudo usermod -aG docker $USER
7_step7.md
Step 7: Check the installation
Close the open terminal on Ubuntu.

Restart WSL via the Windows command line (Powershell).

wsl --shutdown
Access Ubuntu again. Check if Docker was installed correctly on the Ubuntu terminal:

docker --version
You should get a response similar to this:

Docker version 26.1.4, build 5650f9b
8_extra_tips.md
Extra tips
Docker start up and shut down
To start the Docker service run the following on the Ubuntu terminal:

sudo service docker start
To stop the Docker service run the following on the Ubuntu terminal:

sudo service docker stop
Projects location
The performance of WSL 2 lies on running everything within Linux, so avoid running your projects with Docker from the /mnt/c path, as you will lose performance.

Opening folders via terminal
You can open a folder from Ubuntu with Windows Explorer by typing the command on your Ubuntu terminal:

explorer.exe .
The folder will be open using the Windows Explorer.

Remember to navigate to the desired folder on Ubuntu terminal beforehand.

Copy folder from Windows to Ubuntu
On the Ubuntu terminal confirm that you can access the mounted drive and all its directories using the command below.

sudo ls /mnt/*
You have to see the list of folders and files currently present on your Windows C:/ folder.

If you can see the items just fine, then navigate until the destination folder on the Ubuntu terminal and use the following command.

cp -r /mnt/c/my-folder .
Where "my-folder" is the name of the folder on Windows that you want to copy and "." indicates the destination. Since that we are already on the destination folder we can use just "." , but you can inform the desetination path too.

cp -r /mnt/c/my-folder /home/my-user/my-folder
Opening project on Visual Studio Code
You can open a project with the IDE Visual Studio Code by typing the command on your Ubuntu terminal:

code .
Remember to navigate to the desired folder on Ubuntu terminal beforehand.

Free cached memory on Ubuntu
To free cache memory on Linux Ubuntu running on WSL you can use the following command on the Ubuntu terminal:

echo 1 | sudo tee /proc/sys/vm/drop_caches
Windows Terminal
To access your environment through Windows, I recommend using the Windows Terminal by Microsoft, also available on the Windows Store. This tool includes CLI tabs, a high degree of customization, and even native WSL support to open Linux-based windows.

Want to learn more?
If you want to see the official documentation, visit https://docs.docker.com/desktop/wsl/
