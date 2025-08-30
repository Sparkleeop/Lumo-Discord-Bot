import discord
from discord.ext import commands
from discord import app_commands

class ServerInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="serverinfo", description="Displays information about the server.")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild

        embed = discord.Embed(
            title=f"<:discord:1335168663002546199> Server Information - {guild.name}",
            color=discord.Color.blue(),
            timestamp=interaction.created_at
        )

        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

        embed.add_field(name="<:earth_cube:1335169800766226473> Server ID", value=guild.id, inline=False)
        embed.add_field(name="<:wincrown:1335165207630057584> Owner", value=guild.owner.mention, inline=False)
        embed.add_field(name="<:Contact:1335165340199686184> Members", value=guild.member_count, inline=False)
        embed.add_field(name="<:purpleheart:1335169803014504490> Roles", value=len(guild.roles), inline=False)
        embed.add_field(name="<:launch:1154044036441722922> Boost Level", value=guild.premium_tier, inline=False)
        embed.add_field(name="<:clockmc:1335168669369765961> Created On", value=guild.created_at.strftime("%B %d, %Y"), inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(ServerInfo(bot))
