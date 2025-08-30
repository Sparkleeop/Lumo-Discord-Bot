import discord
import asyncio
from discord.ext import commands
from config import TOKEN

# Set up bot with intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

# Use `commands.Bot` but disable prefix commands by setting `command_prefix=None`
bot = commands.Bot(command_prefix=None, intents=intents)

# List of cogs
COGS = ["cogs.moderation", "cogs.minecraft", "cogs.utility", "cogs.triggers", "cogs.welcomer", "cogs.roles", "cogs.afk", "cogs.slowmode", "cogs.lock", "cogs.dm", "cogs.nick", "cogs.warn", "cogs.say", "cogs.anti-link", "cogs.avatar-srvicon", "cogs.serverinfo"]

async def load_cogs():
    """Loads all cogs asynchronously before syncing commands."""
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"✅ Loaded {cog}")
        except Exception as e:
            print(f"❌ Failed to load {cog}: {e}")

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Game(name="Lumo")
    )
    print(f"✅ Logged in as {bot.user}")
    await bot.tree.sync()  # Sync slash commands after cogs are loaded
    commands_list = [cmd.name for cmd in bot.tree.get_commands()]
    print(f"✅ Slash commands synced: {len(commands_list)} commands registered!")
    print("📜 Commands:", ", ".join(commands_list))

# Add the /help command
@bot.tree.command(name="help", description="Show all available commands")
async def help_command(interaction: discord.Interaction):
    commands_list = [f"`/{cmd.name}` - {cmd.description}" for cmd in bot.tree.get_commands()]
    embed = discord.Embed(title="📜 Command List", description="\n".join(commands_list), color=discord.Color.blue())
    await interaction.response.send_message(embed=embed, ephemeral=True)

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())  # Start the bot properly
