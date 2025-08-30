import discord
from discord.ext import commands

class Triggers(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Hardcoded trigger words (all comparisons are done in lowercase)
        self.trigger_store = "store"
        self.trigger_ip = "ip"
        self.trigger_info = "info"

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages from bots to prevent loops
        if message.author.bot:
            return

        content = message.content.lower()

        # Trigger for the store link embed
        if self.trigger_store in content:
            embed = discord.Embed(
                title="Our Store",
                description="Check out our store for exclusive items!\n[Visit Store](https://store.store.yourstore.com)",
                color=discord.Color.blue()
            )
            # You can include custom emojis in the text as long as the bot has access to them.
            embed.add_field(name="Store", value="Get yours today!", inline=False)
            await message.channel.send(embed=embed)

        # Trigger for the server IP embed
        if self.trigger_ip in content:
            embed = discord.Embed(
                title="Server IP",
                description="Join our server using the following IP:",
                color=discord.Color.green()
            )
            embed.add_field(name="IP", value="play.yourserver.com", inline=False)
            await message.channel.send(embed=embed)

        # Trigger for the server info embed
        if self.trigger_info in content:
            embed = discord.Embed(
                title="Server Info",
                description="Learn more about our server and what we offer.",
                color=discord.Color.purple()
            )
            embed.add_field(name="Info", value="Visit our info page for details.", inline=False)
            await message.channel.send(embed=embed)

        # Process other commands if they exist
        await self.bot.process_commands(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Triggers(bot))
