import discord

from discord.ext import commands

import aiohttp

import re

LOG_CHANNEL_ID = 1339647075784327301  # Log channel ID

class EmojiStealer(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @discord.app_commands.command(

        name="addemoji",

        description="Steal a custom emoji from another server and add it here."

    )

    async def addemoji(self, interaction: discord.Interaction, emoji: str):

        # Extract the emoji's details using a regex.

        # The pattern matches both static and animated emojis: <a:name:id> or <:name:id>

        pattern = r"<(a?):(\w+):(\d+)>"

        match = re.fullmatch(pattern, emoji)

        if not match:

            await interaction.response.send_message(

                "❌ Invalid emoji format. Please provide a custom emoji.",

                ephemeral=True

            )

            return

        animated_flag, emoji_name, emoji_id = match.groups()

        file_extension = "gif" if animated_flag == "a" else "png"

        emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{file_extension}?v=1"

        # Fetch the emoji image bytes using aiohttp.

        try:

            async with aiohttp.ClientSession() as session:

                async with session.get(emoji_url) as response:

                    if response.status != 200:

                        await interaction.response.send_message(

                            "❌ Failed to retrieve the emoji image.",

                            ephemeral=True

                        )

                        return

                    image_bytes = await response.read()

        except Exception as e:

            await interaction.response.send_message(

                f"❌ Error fetching emoji: {e}",

                ephemeral=True

            )

            return

        # Create the emoji in the current guild.

        try:

            new_emoji = await interaction.guild.create_custom_emoji(

                name=emoji_name,

                image=image_bytes

            )

        except discord.Forbidden:

            await interaction.response.send_message(

                "❌ I do not have permission to create emojis in this server.",

                ephemeral=True

            )

            return

        except discord.HTTPException as e:

            await interaction.response.send_message(

                f"❌ Failed to create emoji: {e}",

                ephemeral=True

            )

            return

        # Respond with confirmation.

        confirm_embed = discord.Embed(

            title="Emoji Added Successfully!",

            description=f"Added emoji `{new_emoji.name}` {new_emoji}",

            color=discord.Color.green()

        )

        await interaction.response.send_message(embed=confirm_embed)

        # Log the action in the log channel.

        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)

        if log_channel:

            log_embed = discord.Embed(

                title="Emoji Stealer Log",

                description=f"{interaction.user.mention} added emoji `{new_emoji.name}` {new_emoji} to the server.",

                color=discord.Color.blue()

            )

            await log_channel.send(embed=log_embed)

        else:

            print("Log channel not found.")

async def setup(bot: commands.Bot):

    await bot.add_cog(EmojiStealer(bot))

