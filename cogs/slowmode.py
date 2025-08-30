import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Slowmode(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel_id = 1339647075784327301

    async def log_action(self, embed: discord.Embed):
        log_channel = self.bot.get_channel(self.log_channel_id)
        if log_channel:
            await log_channel.send(embed=embed)
        else:
            print("Log channel not found")

    @app_commands.command(
        name="slowmode",
        description="Set slowmode delay in seconds for this channel (0 to disable slowmode)"
    )
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: int):
        # Validate the input (Discord allows 0-21600 seconds)
        if seconds < 0 or seconds > 21600:
            embed = discord.Embed(
                title="❌ Invalid Time",
                description="Please enter a number between 0 and 21600 seconds.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            await interaction.channel.edit(slowmode_delay=seconds)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to update slowmode: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Create an embed for the command response.
        if seconds == 0:
            response_embed = discord.Embed(
                title="🚀 Slowmode Disabled",
                description=f"✅ Slowmode has been turned off in {interaction.channel.mention}.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
        else:
            response_embed = discord.Embed(
                title="⏳ Slowmode Updated",
                description=f"✅ Slowmode set to **{seconds} seconds** in {interaction.channel.mention}.",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )
        await interaction.response.send_message(embed=response_embed)

        # Log the action.
        log_embed = discord.Embed(
            title="Slowmode Update",
            description=f"{interaction.user.mention} set slowmode to `{seconds}` seconds in {interaction.channel.mention}.",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.utcnow()
        )
        await self.log_action(log_embed)

    @slowmode.error
    async def slowmode_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="❌ Permission Denied",
                description="You need the Manage Channels permission to use this command.",
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="❌ Error",
                description=str(error),
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Slowmode(bot))
