import discord
from discord.ext import commands

class AvatarServerIcon(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="avatar", description="Get a user's avatar")
    async def avatar(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user  # If no user is mentioned, use the command sender

        embed = discord.Embed(
            title=f"{user.display_name}'s Avatar",
            color=discord.Color.blue()
        )
        embed.set_image(url=user.avatar.url)
        embed.set_footer(text=f"Requested by {interaction.user.name}")

        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name="servericon", description="Get the server's icon")
    async def servericon(self, interaction: discord.Interaction):
        if interaction.guild.icon is None:
            await interaction.response.send_message("This server has no icon.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"{interaction.guild.name}'s Server Icon",
            color=discord.Color.blue()
        )
        embed.set_image(url=interaction.guild.icon.url)
        embed.set_footer(text=f"Requested by {interaction.user.name}")

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(AvatarServerIcon(bot))
