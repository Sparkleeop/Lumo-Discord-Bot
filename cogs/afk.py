import discord
from discord.ext import commands

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Remove AFK when user sends a message
        if message.author.id in self.afk_users:
            embed = discord.Embed(
                title="Welcome Back!",
                description="✅ You are no longer AFK.",
                color=discord.Color.green()
            )
            await message.channel.send(embed=embed)
            del self.afk_users[message.author.id]

        # Notify if a mentioned user is AFK
        for mention in message.mentions:
            if mention.id in self.afk_users:
                reason = self.afk_users[mention.id]
                embed = discord.Embed(
                    title="AFK Alert",
                    description=f"🚀 **{mention.display_name}** is currently AFK.\n**Reason:** {reason}",
                    color=discord.Color.orange()
                )
                await message.channel.send(embed=embed)

    @commands.hybrid_command(name="afk", description="Set your AFK status")
    async def afk(self, ctx, *, reason: str = "No reason provided"):
        self.afk_users[ctx.author.id] = reason
        embed = discord.Embed(
            title="AFK Set",
            description=f"🌙 **{ctx.author.display_name}** is now AFK.\n**Reason:** {reason}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AFK(bot))
