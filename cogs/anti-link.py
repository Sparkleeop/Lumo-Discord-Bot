import discord
from discord.ext import commands
import re
import datetime
import asyncio

class AntiLink(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.exempt_role_id = 1339688281922736209  # Role ID exempt from anti-link
        self.log_channel_id = 1339647075784327301  # Log channel ID
        self.muted_role_name = "Muted"  # Name of the mute role
        # A basic regex pattern to detect links
        self.link_pattern = re.compile(r'https?://\S+')

    def has_exempt_role(self, member: discord.Member) -> bool:
        return any(role.id == self.exempt_role_id for role in member.roles)

    async def get_or_create_muted_role(self, guild: discord.Guild) -> discord.Role:
        muted_role = discord.utils.get(guild.roles, name=self.muted_role_name)
        if not muted_role:
            muted_role = await guild.create_role(name=self.muted_role_name, reason="Created for anti-link system")
            # Deny sending messages, speaking, and adding reactions in all channels
            for channel in guild.channels:
                try:
                    await channel.set_permissions(muted_role, send_messages=False, speak=False, add_reactions=False)
                except Exception as e:
                    print(f"Failed to set permissions for {channel.name}: {e}")
        return muted_role

    async def log_action(self, embed: discord.Embed):
        log_channel = self.bot.get_channel(self.log_channel_id)
        if log_channel:
            await log_channel.send(embed=embed)
        else:
            print("Log channel not found.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages from bots
        if message.author.bot:
            return

        # Check if the author has the exempt role; if yes, do nothing.
        if self.has_exempt_role(message.author):
            return

        # Check if the message contains a link
        if self.link_pattern.search(message.content):
            # Delete the message
            try:
                await message.delete()
            except Exception as e:
                print(f"Failed to delete message: {e}")

            # Mute the user by giving them the muted role
            muted_role = await self.get_or_create_muted_role(message.guild)
            try:
                await message.author.add_roles(muted_role, reason="Anti-link system triggered")
            except Exception as e:
                print(f"Failed to add muted role to {message.author}: {e}")
                return

            # Send a warning embed in the channel
            warning_embed = discord.Embed(
                title="Muted by Anti-Link System",
                description=f"🚫 {message.author.mention}, you have been muted for sending a link.",
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            await message.channel.send(embed=warning_embed)

            # Log the action in the log channel
            log_embed = discord.Embed(
                title="Anti-Link Triggered",
                description=f"{message.author.mention} was muted for sending a link in {message.channel.mention}.",
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            await self.log_action(log_embed)

            # DM the user to notify them of the mute
            dm_embed = discord.Embed(
                title="You have been muted",
                description=(
                    f"You have been muted in **{message.guild.name}** for sending a link.\n"
                    "Please refrain from posting links. If you believe this is a mistake, contact a moderator."
                ),
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            try:
                await message.author.send(embed=dm_embed)
            except Exception as e:
                print(f"Failed to DM {message.author}: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(AntiLink(bot))
