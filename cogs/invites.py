import discord

from discord.ext import commands

import json

class InviteTracker(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

        self.invites = {}

        self.load_invites()

    def load_invites(self):

        try:

            with open("invites.json", "r") as f:

                self.invites = json.load(f)

        except FileNotFoundError:

            self.invites = {}

    def save_invites(self):

        with open("invites.json", "w") as f:

            json.dump(self.invites, f, indent=4)

    @commands.Cog.listener()

    async def on_ready(self):

        for guild in self.bot.guilds:

            self.invites[guild.id] = await guild.invites()

    @commands.Cog.listener()

    async def on_member_join(self, member: discord.Member):

        guild = member.guild

        new_invites = await guild.invites()

        old_invites = self.invites.get(str(guild.id), [])

        inviter = None

        for invite in new_invites:

            for old_invite in old_invites:

                if invite.code == old_invite.code and invite.uses > old_invite.uses:

                    inviter = invite.inviter

                    break

        self.invites[str(guild.id)] = new_invites

        self.save_invites()

        if inviter:

            inviter_id = str(inviter.id)

            if inviter_id not in self.invites:

                self.invites[inviter_id] = 0

            self.invites[inviter_id] += 1

            self.save_invites()

            log_channel = discord.utils.get(guild.text_channels, name="invite-logs")

            if log_channel:

                embed = discord.Embed(

                    title="New Member Joined",

                    description=f"{member.mention} joined using {inviter.mention}'s invite!",

                    color=discord.Color.green()

                )

                await log_channel.send(embed=embed)

    @commands.hybrid_command(name="invites", description="Check how many invites a user has.")

    async def invites(self, ctx, member: discord.Member = None):

        member = member or ctx.author

        invite_count = self.invites.get(str(member.id), 0)

        embed = discord.Embed(

            title=f"{member.display_name}'s Invites",

            description=f"{member.mention} has invited **{invite_count}** members!",

            color=discord.Color.blue()

        )

        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):

    await bot.add_cog(InviteTracker(bot))

