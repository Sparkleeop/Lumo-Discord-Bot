import discord
from discord import app_commands
from discord.ext import commands
import datetime

class Lock(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel_id = 1339647075784327301

    async def log_action(self, embed: discord.Embed):
        log_channel = self.bot.get_channel(self.log_channel_id)
        if log_channel:
            await log_channel.send(embed=embed)
        else:
            print("Log channel not found")

    @app_commands.command(name="lock", description="Lock a channel so no normal user can send messages.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        target_channel = channel or interaction.channel
        everyone = interaction.guild.default_role
        overwrite = target_channel.overwrites_for(everyone)
        overwrite.send_messages = False
        try:
            await target_channel.edit(overwrites={everyone: overwrite})
            embed = discord.Embed(
                title="Channel Locked",
                description=f"{target_channel.mention} has been locked.",
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.response.send_message(embed=embed)
            
            log_embed = discord.Embed(
                title="Lock Action",
                description=f"{interaction.user.mention} locked {target_channel.mention}.",
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            await self.log_action(log_embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Could not lock channel: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unlock", description="Unlock a channel so normal users can send messages again.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        target_channel = channel or interaction.channel
        everyone = interaction.guild.default_role
        overwrite = target_channel.overwrites_for(everyone)
        overwrite.send_messages = None
        try:
            await target_channel.edit(overwrites={everyone: overwrite})
            embed = discord.Embed(
                title="Channel Unlocked",
                description=f"{target_channel.mention} has been unlocked.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.response.send_message(embed=embed)
            
            log_embed = discord.Embed(
                title="Unlock Action",
                description=f"{interaction.user.mention} unlocked {target_channel.mention}.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            await self.log_action(log_embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Could not unlock channel: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Lock(bot))
