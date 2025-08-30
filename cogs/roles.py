import discord
from discord.ext import commands
import datetime

class RoleManagement(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel_id = 1339647075784327301  # Log channel ID

    async def log_action(self, embed: discord.Embed):
        """Helper function to send log embed to the specified log channel."""
        log_channel = self.bot.get_channel(self.log_channel_id)
        if log_channel:
            await log_channel.send(embed=embed)
        else:
            print("Log channel not found")

    @discord.app_commands.command(name="addrole", description="Add a role to a member")
    @discord.app_commands.checks.has_permissions(manage_roles=True)
    async def addrole(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        try:
            await member.add_roles(role)
            embed = discord.Embed(
                title="Role Added",
                description=f"{role.mention} has been added to {member.mention}.",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            # Log the action
            log_embed = discord.Embed(
                title="Moderation Log: Role Added",
                description=f"{interaction.user.mention} added {role.mention} to {member.mention}.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            await self.log_action(log_embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Failed to add role: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.app_commands.command(name="removerole", description="Remove a role from a member")
    @discord.app_commands.checks.has_permissions(manage_roles=True)
    async def removerole(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        try:
            await member.remove_roles(role)
            embed = discord.Embed(
                title="Role Removed",
                description=f"{role.mention} has been removed from {member.mention}.",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            # Log the action
            log_embed = discord.Embed(
                title="Moderation Log: Role Removed",
                description=f"{interaction.user.mention} removed {role.mention} from {member.mention}.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            await self.log_action(log_embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Failed to remove role: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(RoleManagement(bot))
