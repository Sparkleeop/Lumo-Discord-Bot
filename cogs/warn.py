import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import datetime
from config import LOGS

class Warns(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.file = "warns.json"
        self.log_channel_id = LOGS
        # Ensure the JSON file exists
        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump({}, f)

    def load_warns(self) -> dict:
        with open(self.file, "r") as f:
            return json.load(f)

    def save_warns(self, data: dict) -> None:
        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    async def log_action(self, embed: discord.Embed) -> None:
        log_channel = self.bot.get_channel(self.log_channel_id)
        if log_channel:
            await log_channel.send(embed=embed)
        else:
            print("Moderation log channel not found.")

    @app_commands.command(name="warn", description="Warn a user with a reason.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        data = self.load_warns()
        guild_id = str(interaction.guild.id)
        user_id = str(user.id)
        if guild_id not in data:
            data[guild_id] = {}
        if user_id not in data[guild_id]:
            data[guild_id][user_id] = []
        warn_id = len(data[guild_id][user_id]) + 1
        warn_entry = {
            "warn_id": warn_id,
            "reason": reason,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "moderator": str(interaction.user.id)
        }
        data[guild_id][user_id].append(warn_entry)
        self.save_warns(data)
        
        # Send confirmation in the channel.
        embed = discord.Embed(
            title="User Warned",
            description=f"{user.mention} has been warned.\n**Warn ID:** {warn_id}\n**Reason:** {reason}",
            color=discord.Color.orange(),
            timestamp=datetime.datetime.utcnow()
        )
        await interaction.response.send_message(embed=embed)
        
        # Log the warn action.
        log_embed = discord.Embed(
            title="Moderation Log: Warn",
            description=f"{interaction.user.mention} warned {user.mention}.",
            color=discord.Color.orange(),
            timestamp=datetime.datetime.utcnow()
        )
        log_embed.add_field(name="Reason", value=reason, inline=False)
        await self.log_action(log_embed)
        
        # Attempt to DM the warned user with an embed.
        dm_embed = discord.Embed(
            title="You have been warned",
            description=(
                f"You have received a warn in **{interaction.guild.name}**.\n"
                f"**Warn ID:** {warn_id}\n"
                f"**Reason:** {reason}"
            ),
            color=discord.Color.orange(),
            timestamp=datetime.datetime.utcnow()
        )
        try:
            await user.send(embed=dm_embed)
        except Exception as e:
            print(f"Failed to DM {user}: {e}")

    @app_commands.command(name="listwarn", description="List all warns for a user.")
    async def listwarn(self, interaction: discord.Interaction, user: discord.Member):
        data = self.load_warns()
        guild_id = str(interaction.guild.id)
        user_id = str(user.id)
        if guild_id not in data or user_id not in data[guild_id] or len(data[guild_id][user_id]) == 0:
            embed = discord.Embed(
                title="Warns",
                description=f"{user.mention} has no warns.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.response.send_message(embed=embed)
        else:
            warns = data[guild_id][user_id]
            description = ""
            for warn in warns:
                moderator_mention = f"<@{warn['moderator']}>"
                description += (
                    f"**ID:** {warn['warn_id']} | **Reason:** {warn['reason']} | "
                    f"**Moderator:** {moderator_mention} | **Time:** {warn['timestamp']}\n"
                )
            embed = discord.Embed(
                title=f"Warns for {user.display_name}",
                description=description,
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clearwarn", description="Clear a specific warn for a user by warn ID.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clearwarn(self, interaction: discord.Interaction, user: discord.Member, warn_id: int):
        data = self.load_warns()
        guild_id = str(interaction.guild.id)
        user_id = str(user.id)
        if guild_id not in data or user_id not in data[guild_id]:
            embed = discord.Embed(
                title="No Warns",
                description=f"{user.mention} has no warns.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.response.send_message(embed=embed)
            return
        else:
            warns = data[guild_id][user_id]
            found = False
            for i, warn in enumerate(warns):
                if warn["warn_id"] == warn_id:
                    found = True
                    del warns[i]
                    break
            if not found:
                embed = discord.Embed(
                    title="Warn Not Found",
                    description=f"No warn with ID {warn_id} found for {user.mention}.",
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
                await interaction.response.send_message(embed=embed)
                return
            # Reassign warn IDs sequentially
            for index, warn in enumerate(warns):
                warn["warn_id"] = index + 1
            data[guild_id][user_id] = warns
            self.save_warns(data)
            embed = discord.Embed(
                title="Warn Cleared",
                description=f"Warn ID {warn_id} has been cleared for {user.mention}.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.response.send_message(embed=embed)
            
            log_embed = discord.Embed(
                title="Moderation Log: Clear Warn",
                description=f"{interaction.user.mention} cleared warn ID {warn_id} for {user.mention}.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            await self.log_action(log_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Warns(bot))
