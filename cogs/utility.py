import discord
from discord import app_commands
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="userinfo", description="Get user information")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        embed = discord.Embed(title=f"User Info - {member}", color=discord.Color.blue())
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
