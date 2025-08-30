import discord
from discord import app_commands
from discord.ext import commands
import datetime

class Say(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel_id = 1339647075784327301  # Log channel ID

    async def log_action(self, embed: discord.Embed):
        log_channel = self.bot.get_channel(self.log_channel_id)
        if log_channel:
            await log_channel.send(embed=embed)
        else:
            print("Log channel not found.")

    @app_commands.command(name="say", description="Make the bot say a message in the current channel.")
    @app_commands.checks.has_permissions(administrator=True)
    async def say(self, interaction: discord.Interaction, message: str):
        try:
            # Send the message as the bot in the current channel
            await interaction.channel.send(message)
            
            # Create and send a log embed
            log_embed = discord.Embed(
                title="Moderation Log: Say Command",
                description=f"{interaction.user.mention} used `/say` with message:\n```{message}```",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )
            await self.log_action(log_embed)
            
            # Acknowledge the command to the invoker
            await interaction.response.send_message("✅ Message sent!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error sending message: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Say(bot))
