import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # The ID of the channel where welcome messages will be sent
        self.channel_id = 1334420286514397256

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # Get the channel by ID
        channel = member.guild.get_channel(self.channel_id)
        if channel is None:
            return  # Channel not found; perhaps log an error or warning

        # Create the welcome message. The member mention is included via member.mention.
        welcome_message = (
            f"<:adorable:1335168668153282661> Welcome **{member.mention}** to WildBlocksMC. Make sure you read our rules!\n\n"
            f"<:icecube:1335169794382630923> **Join us on** `play.wildblocks.fun`"
        )
        await channel.send(welcome_message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))
