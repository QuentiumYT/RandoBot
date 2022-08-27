import nextcord, os, asyncio
from nextcord.ext import commands
from cogwatch import watch

from cogs.utils import config, cogs

__author__ = "QuentiumYT"
__version__ = "2.0.0"



class RandoBot(commands.Bot):
    def __init__(self):
        intents = nextcord.Intents.all()

        super().__init__(
            command_prefix="-",
            description="Rando Bot",
            owner_id=246943045105221633,
            help_command=None,
            case_insensitive=True,
            max_messages=999999,
            intents=intents,
        )

    @watch(path="cogs")
    async def on_ready(self):
        print("Logged in as %s#%s" % (self.user.name, self.user.discriminator))

        await self.change_presence(
            status=nextcord.Status.online,
            activity=nextcord.Activity(
                name="Prépare une rando...",
                type=nextcord.ActivityType.playing
            )
        )

    async def on_raw_reaction_add(self, ctx):
        if not ctx.member.bot:
            if any(ctx.emoji.name == x for x in ["Check", "Average"]):
                role = nextcord.utils.get(ctx.member.guild.roles, name=config["role_next_rando"])
                try:
                    await ctx.member.add_roles(role)
                except nextcord.errors.Forbidden:
                    pass

    async def on_raw_reaction_remove(self, ctx):
        guild = nextcord.utils.get(self.guilds, id=ctx.guild_id)
        user = nextcord.utils.get(guild.members, id=ctx.user_id)
        if not user.bot:
            if any(ctx.emoji.name == x for x in ["Check", "Average", "Cross"]):
                role = nextcord.utils.get(guild.roles, name=config["role_next_rando"])
                try:
                    await user.remove_roles(role)
                except nextcord.errors.Forbidden:
                    pass



async def main():
    bot = RandoBot()

    for cog in cogs:
        bot.load_extension("cogs." + cog)

    await bot.start(os.environ.get("TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
