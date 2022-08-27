import nextcord, os
from nextcord.ext import commands

from cogs.utils import config, cogs

__author__ = "QuentiumYT"
__version__ = "2.0.0"



intents = nextcord.Intents.all()

bot = commands.Bot(
    command_prefix="-",
    description="Rando Bot",
    owner_id=246943045105221633,
    help_command=None,
    case_insensitive=True,
    max_messages=999999,
    intents=intents,
)

@bot.event
async def on_ready():
    print("Logged in as %s#%s" % (bot.user.name, bot.user.discriminator))

    await bot.change_presence(
        status=nextcord.Status.online,
        activity=nextcord.Activity(
            name="Prépare une rando...",
            type=nextcord.ActivityType.playing
        )
    )

@bot.event
async def on_raw_reaction_add(ctx):
    if not ctx.member.bot:
        if any(ctx.emoji.name == x for x in ["Check", "Average"]):
            role = nextcord.utils.get(ctx.member.guild.roles, name=config["role_next_rando"])
            try:
                await ctx.member.add_roles(role)
            except nextcord.errors.Forbidden:
                pass

@bot.event
async def on_raw_reaction_remove(ctx):
    guild = nextcord.utils.get(bot.guilds, id=ctx.guild_id)
    user = nextcord.utils.get(guild.members, id=ctx.user_id)
    if not user.bot:
        if any(ctx.emoji.name == x for x in ["Check", "Average", "Cross"]):
            role = nextcord.utils.get(guild.roles, name=config["role_next_rando"])
            try:
                await user.remove_roles(role)
            except nextcord.errors.Forbidden:
                pass



if __name__ == "__main__":
    for cog in cogs:
        bot.load_extension("cogs." + cog)

    bot.run(os.environ.get("TOKEN"))
