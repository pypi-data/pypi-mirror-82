import asyncio

import discord
from discord.ext import commands

from . import utils


class BotSettings(utils.Cog):

    @commands.command(cls=utils.Command)
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(send_messages=True)
    @commands.guild_only()
    async def prefix(self, ctx:utils.Context, *, new_prefix:str):
        """
        Changes the prefix that the bot uses.
        """

        # Validate prefix
        if len(new_prefix) > 30:
            return await ctx.send("The maximum length a prefix can be is 30 characters.")

        # Store setting
        self.bot.guild_settings[ctx.guild.id]['prefix'] = new_prefix
        async with self.bot.database() as db:
            await db("INSERT INTO guild_settings (guild_id, prefix) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET prefix=excluded.prefix", ctx.guild.id, new_prefix)
        await ctx.send(f"My prefix has been updated to `{new_prefix}`.")

    @commands.command(cls=utils.Command, aloases=['follow'])
    @commands.has_permissions(manage_guild=True, manage_channels=True)
    @commands.bot_has_permissions(send_messages=True, add_reactions=True, manage_channels=True)
    @commands.guild_only()
    @utils.checks.is_config_set('command_data', 'updates_channel_id')
    async def updates(self, ctx:utils.Context):
        """
        Get official bot updates from the support server.
        """

        # See if they're sure
        m = await ctx.send(f"This will follow the bot's official updates channel from the support server (`{ctx.clean_prefix}support`). Would you like to continue?")
        valid_emojis = ["\N{THUMBS UP SIGN}", "\N{THUMBS DOWN SIGN}"]
        for e in valid_emojis:
            await m.add_reaction(e)
        try:
            reaction, _ = await self.bot.wait_for("reaction_add", check=lambda r, u: str(r.emoji) in valid_emojis and u.id == ctx.author.id and r.message.id == m.id, timeout=120)
        except asyncio.TimeoutError:
            try:
                await m.delete()
            except discord.HTTPException:
                pass
            return

        # Cancel follow
        if str(reaction) == "\N{THUMBS DOWN SIGN}":
            return await ctx.send("Alright, cancelling!", ignore_error=True)

        # Get channel
        channel_id = self.bot.config['command_data']['updates_channel_id']
        try:
            channel = self.bot.get_channel(channel_id) or await self.bot.fetch_channel(channel_id)
            assert channel.is_news()
        except Exception:
            return await ctx.send("I couldn't reach the updates channel!")

        # Follow it
        try:
            await channel.follow(destination=ctx.channel)
        except discord.HTTPException as e:
            return await ctx.send(f"I wasn't able to follow the updates channel - {e}")

        # Output message
        try:
            await self.bot.wait_for("message", check=lambda m: m.content == f"{channel.guild.name} #{channel.name}", timeout=5)
        except asyncio.TimeoutError:
            pass
        try:
            await m.delete()
        except discord.HTTPException:
            pass
        return await ctx.send("Now following the bot's updates channel!", ignore_error=True)


def setup(bot:utils.Bot):
    x = BotSettings(bot)
    bot.add_cog(x)
