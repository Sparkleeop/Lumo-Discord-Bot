import discord
from discord import app_commands
from discord.ext import commands
import datetime

class Nicknames(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel_id = 1339647075784327301

    async def log_action(self, embed: discord.Embed):
        log_channel = self.bot.get_channel(self.log_channel_id)
        if log_channel:
            await log_channel.send(embed=embed)
        else:
            print("Log channel not found")

    @app_commands.command(name="nick", description="Set your nickname or another user's nickname")
    async def nick(self, interaction: discord.Interaction, name: str, user: discord.Member = None):
        target = user or interaction.user
        if target != interaction.user:
            if not interaction.user.guild_permissions.manage_nicknames:
                embed = discord.Embed(
                    title="Permission Denied",
                    description="You do not have permission to change others' nicknames.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

        try:
            await target.edit(nick=name)
            if target == interaction.user:
                embed = discord.Embed(
                    title="Nickname Updated",
                    description=f"✅ Your nickname has been changed to **{name}**.",
                    color=discord.Color.green(),
                    timestamp=datetime.datetime.utcnow()
                )
            else:
                embed = discord.Embed(
                    title="Nickname Updated",
                    description=f"✅ {target.mention}'s nickname has been changed to **{name}**.",
                    color=discord.Color.green(),
                    timestamp=datetime.datetime.utcnow()
                )
            await interaction.response.send_message(embed=embed)
            
            log_embed = discord.Embed(
                title="Nickname Change",
                description=f"{interaction.user.mention} changed {target.mention}'s nickname to **{name}**.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            await self.log_action(log_embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"❌ Failed to change nickname: {e}",
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Nicknames(bot))
