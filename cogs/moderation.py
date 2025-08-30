import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Channel ID where moderation logs will be sent.
        self.log_channel_id = 1339647075784327301

    def log_action(self, embed: discord.Embed) -> None:
        """Helper to send a log embed to the moderation log channel."""
        log_channel = self.bot.get_channel(self.log_channel_id)
        if log_channel is None:
            # If not found via bot.get_channel, try fetching from guilds.
            for guild in self.bot.guilds:
                log_channel = guild.get_channel(self.log_channel_id)
                if log_channel:
                    break
        if log_channel:
            asyncio.create_task(log_channel.send(embed=embed))
        else:
            print("Moderation log channel not found.")

    @app_commands.command(name="kick", description="Kick a member")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="User Kicked",
            description=f"✅ {member.mention} has been kicked.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        
        # Log action
        log_embed = discord.Embed(
            title="Moderation Log: Kick",
            description=f"**Moderator:** {interaction.user.mention}\n**Target:** {member.mention}",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        log_embed.add_field(name="Reason", value=reason, inline=False)
        self.log_action(log_embed)

    @app_commands.command(name="ban", description="Ban a member")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="User Banned",
            description=f"✅ {member.mention} has been banned.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        
        log_embed = discord.Embed(
            title="Moderation Log: Ban",
            description=f"**Moderator:** {interaction.user.mention}\n**Target:** {member.mention}",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        log_embed.add_field(name="Reason", value=reason, inline=False)
        self.log_action(log_embed)

    @app_commands.command(name="purge", description="Delete messages in bulk")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.purge(limit=amount)
        embed = discord.Embed(
            title="Messages Purged",
            description=f"✅ Deleted {amount} messages.",
            color=discord.Color.orange()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        
        log_embed = discord.Embed(
            title="Moderation Log: Purge",
            description=f"**Moderator:** {interaction.user.mention}\n**Channel:** {interaction.channel.mention}",
            color=discord.Color.orange(),
            timestamp=datetime.datetime.utcnow()
        )
        log_embed.add_field(name="Amount", value=str(amount), inline=False)
        self.log_action(log_embed)

    @app_commands.command(name="mute", description="Mute a member using a role-based method")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await interaction.guild.create_role(name="Muted")
            # Apply channel overrides for the muted role in every channel.
            for channel in interaction.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)
        await member.add_roles(muted_role, reason=reason)
        embed = discord.Embed(
            title="User Muted",
            description=f"✅ {member.mention} has been muted.",
            color=discord.Color.dark_gray()
        )
        await interaction.response.send_message(embed=embed)
        
        log_embed = discord.Embed(
            title="Moderation Log: Mute",
            description=f"**Moderator:** {interaction.user.mention}\n**Target:** {member.mention}",
            color=discord.Color.dark_gray(),
            timestamp=datetime.datetime.utcnow()
        )
        log_embed.add_field(name="Reason", value=reason, inline=False)
        self.log_action(log_embed)

    @app_commands.command(name="unmute", description="Unmute a member")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if muted_role and muted_role in member.roles:
            await member.remove_roles(muted_role, reason="Unmute command executed")
            embed = discord.Embed(
                title="User Unmuted",
                description=f"✅ {member.mention} has been unmuted.",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
            
            log_embed = discord.Embed(
                title="Moderation Log: Unmute",
                description=f"**Moderator:** {interaction.user.mention}\n**Target:** {member.mention}",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            self.log_action(log_embed)
        else:
            await interaction.response.send_message("❌ This user is not muted.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
