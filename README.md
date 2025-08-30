# 🌙 Lumo Discord Bot

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/github/license/Sparkleeop/Lumo-Discord-Bot?color=green)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/Sparkleeop/Lumo-Discord-Bot?style=social)](https://github.com/Sparkleeop/Lumo-Discord-Bot/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/Sparkleeop/Lumo-Discord-Bot?color=red)](https://github.com/Sparkleeop/Lumo-Discord-Bot/commits/main)
[![Language](https://img.shields.io/github/languages/top/Sparkleeop/Lumo-Discord-Bot?color=yellow)](https://github.com/Sparkleeop/Lumo-Discord-Bot)

Lumo is a modular, feature-rich Discord bot built using **[discord.py](https://discordpy.readthedocs.io/en/stable/)**.  
It comes with moderation tools, utility commands, role management, and fun features, all organized in cogs.

---

## ✨ Features
- 🔨 **Moderation** – Kick, ban, mute, warn, slowmode, lock channels.
- 🛡️ **Anti-Link** – Prevents unwanted link sharing.
- 👋 **Welcomer** – Sends welcome messages when new members join.
- 🎭 **Roles Management** – Assign and manage server roles.
- 📢 **Announcements** – Say command for broadcasting messages.
- 🕒 **AFK System** – Let others know when you’re AFK.
- 🔍 **Server Info** – Quick overview of server stats.
- 📩 **DM Tools** – Send messages directly via the bot.
- 🎮 **Minecraft Cog** – Minecraft-related utilities.
- 😀 **Emoji Stealer** – Add emojis from other servers.
- ⚡ And much more...

---

## 📂 Project Structure

```
├── bot.py             # Main entry point 
├── config.py          # Bot configuration 
├── requirements.txt   # Python dependencies 
├── cogs/              # Command modules
└── ...
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Sparkleeop/Lumo-Discord-Bot
cd Lumo-Discord-Bot
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a .env file in the project root:

```dotenv
DISCORD_BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN
LOGS_CHANNEL_ID=YOUR_LOGS_CHANNEL_ID
EXEMPT_ROLE_ID=YOUR_EXEMPT_ROLE_ID
DM_ROLE_ID=YOUR_DM_ROLE_ID
WELCOME_CHANNEL_ID=YOUR_WELCOME_CHANNEL_ID
```

5. Run the bot

```bash
python bot.py
```

---

🛠️ Contributing

Contributions are welcome! 🎉
Here’s how you can help:

1. Fork the repo.


2. Create a new branch (git checkout -b feature/your-feature).


3. Commit your changes (git commit -m "Added new feature").


4. Push to your fork (git push origin feature/your-feature).


5. Open a Pull Request.



Please follow clean code practices and ensure all new features are modular (placed in cogs/).


---

📝 License

This project is licensed under the MIT License, see LICENSE for details.


---

⭐ Support

If you like this project, consider giving it a star ⭐ on GitHub.