import discord
from discord import app_commands
from discord.ext import commands
import datetime
from config import LOGS, DM_ROLE

def check_dm_role(interaction: discord.Interaction) -> bool:
    if not isinstance(interaction.user, discord.Member):
        return False
    required_role_id = DM_ROLE
    return any(role.id == required_role_id for role in interaction.user.roles)

class DM(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel_id = LOGS

    async def log_action(self, embed: discord.Embed):
        log_channel = self.bot.get_channel(self.log_channel_id)
        if log_channel:
            await log_channel.send(embed=embed)
        else:
            print("Log channel not found")

    @app_commands.command(name="dm", description="DM a specified user with a message")
    @app_commands.check(check_dm_role)
    async def dm(self, interaction: discord.Interaction, user: discord.Member, message: str):
        try:
            await user.send(message)
            embed = discord.Embed(
                title="DM Sent",
                description=f"✅ Successfully sent a DM to {user.mention}.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.response.send_message(embed=embed)
            
            log_embed = discord.Embed(
                title="DM Log",
                description=f"{interaction.user.mention} sent a DM to {user.mention}.",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )
            log_embed.add_field(name="Message", value=message, inline=False)
            await self.log_action(log_embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"❌ Failed to DM {user.mention}: {e}",
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.response.send_message(embed=embed)

    @dm.error
    async def dm_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, app_commands.CheckFailure):
            embed = discord.Embed(
                title="Permission Denied",
                description="You do not have the required role to use this command.",
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="Error",
                description=str(error),
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(DM(bot))
