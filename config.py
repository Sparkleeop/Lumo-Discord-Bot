import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
LOGS = os.getenv("LOGS_CHANNEL_ID")
EXEMPT_ROLE = os.getenv("EXEMPT_ROLE_ID")
DM_ROLE = os.getenv("DM_ROLE_ID")
WELCOME_CHANNEL = os.getenv("WELCOME_CHANNEL_ID")

git reset $(git commit-tree HEAD^{tree} -m "Lumo Init")