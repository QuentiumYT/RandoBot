import nextcord
from nextcord.ext import commands

class ManageCogs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="load",
        description="Load a cog into the bot",
        guild_ids=[380373195473027074],
    )
    @commands.is_owner()
    async def load(self, ctx: nextcord.Interaction, extension: str = None):
        if extension:
            try:
                self.bot.load_extension("cogs." + extension)
                return await ctx.send(f"`{extension}` successfully loaded.", ephemeral=True)
            except Exception as e:
                return await ctx.send(f"```py\n{type(e).__name__}: {e}\n```", ephemeral=True)

    @nextcord.slash_command(
        name="unload",
        description="Unload a cog from the bot",
        guild_ids=[380373195473027074],
    )
    @commands.is_owner()
    async def unload(self, ctx: nextcord.Interaction, extension: str = None):
        if extension:
            try:
                self.bot.unload_extension("cogs." + extension)
                return await ctx.send(f"`{extension}` successfully unloaded.", ephemeral=True)
            except Exception as e:
                return await ctx.send(f"```py\n{type(e).__name__}: {e}\n```", ephemeral=True)

    @nextcord.slash_command(
        name="reload",
        description="Reload a cog into the bot",
        guild_ids=[380373195473027074],
    )
    @commands.is_owner()
    async def reload(self, ctx: nextcord.Interaction, extension: str = None):
        if extension:
            try:
                self.bot.unload_extension("cogs." + extension)
                self.bot.load_extension("cogs." + extension)
                return await ctx.send(f"`{extension}` successfully reloaded.", ephemeral=True)
            except Exception as e:
                return await ctx.send(f"```py\n{type(e).__name__}: {e}\n```", ephemeral=True)

def setup(bot):
    bot.add_cog(ManageCogs(bot))
