import nextcord, os, dotenv, json, re
from nextcord.ext import commands
from datetime import date, timedelta

__author__ = "QuentiumYT"

with open("config.json", "r", encoding="utf-8", errors="ignore") as file:
    config = json.loads(file.read(), strict=False)

dotenv.load_dotenv()

intents = nextcord.Intents.all()

client = commands.Bot(
    command_prefix="-",
    description="Rando Bot",
    owner_id=246943045105221633,
    help_command=None,
    case_insensitive=True,
    max_messages=999999,
    intents=intents,
)

def emo(text):
    return str(nextcord.utils.get(client.emojis, name=text))

@client.event
async def on_ready():
    print("Logged in as %s#%s" % (client.user.name, client.user.discriminator))

    await client.change_presence(
        status=nextcord.Status.online,
        activity=nextcord.Activity(
            name="Prépare une rando...",
            type=nextcord.ActivityType.playing
        )
    )

@client.listen()
async def on_message(message: nextcord.Message):
    # Correct channel and mention everyone or role
    if message.channel.id == config["channel_announcements"] and (message.mention_everyone or message.role_mentions):
        if "date" in message.content.lower() or "heure" in message.content.lower():
            if message.author.bot:
                return

            await message.add_reaction(emo("Check"))
            await message.add_reaction(emo("Average"))
            await message.add_reaction(emo("Cross"))

            planned_date = re.findall(r"(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](20\d{2})", message.content)

            category = nextcord.utils.get(message.guild.categories, name=config["category_default"])

            if planned_date:
                # Specified date
                date_obj = date(int(planned_date[0][2]), int(planned_date[0][1]), int(planned_date[0][0]))
            elif "demain" in message.content.lower():
                # Tomorrow date
                date_obj = date.today() + timedelta(days=1)
            elif "samedi" in message.content.lower():
                # Upcoming saturday date
                delta = timedelta(days=5 - date.today().weekday())
                date_obj = date.today() + delta if delta.days > 1 else date.today() + delta + timedelta(days=7)
            elif "dimanche" in message.content.lower():
                # Upcoming sunday date
                delta = timedelta(days=6 - date.today().weekday())
                date_obj = date.today() + delta if delta.days > 1 else date.today() + delta + timedelta(days=7)
            date_repr = date_obj.strftime("%d-%m-%Y")

            channel = await message.guild.create_text_channel("rando-" + date_repr, category=category)

            overwrites = {
                message.guild.default_role: nextcord.PermissionOverwrite(view_channel=True, send_messages=False),
                message.author: nextcord.PermissionOverwrite(view_channel=True, send_messages=True, mention_everyone=True),
                nextcord.utils.get(message.author.guild.roles, name=config["role_next_rando"]): nextcord.PermissionOverwrite(view_channel=True, send_messages=True),
            }

            for target, overwrite in overwrites.items():
                await channel.set_permissions(target, overwrite=overwrite)
        else:
            await message.channel.send("Merci de préciser une date si vous organisez une rando! (jj/mm/aaaa | demain)", delete_after=15)
            await message.delete()

@client.event
async def on_raw_reaction_add(ctx):
    if not ctx.member.bot:
        if any(ctx.emoji.name == x for x in ["Check", "Average"]):
            role = nextcord.utils.get(ctx.member.guild.roles, name=config["role_next_rando"])
            try:
                await ctx.member.add_roles(role)
            except nextcord.errors.Forbidden:
                pass

@client.event
async def on_raw_reaction_remove(ctx):
    guild = nextcord.utils.get(client.guilds, id=ctx.guild_id)
    user = nextcord.utils.get(guild.members, id=ctx.user_id)
    if not user.bot:
        if any(ctx.emoji.name == x for x in ["Check", "Average", "Cross"]):
            role = nextcord.utils.get(guild.roles, name=config["role_next_rando"])
            try:
                await user.remove_roles(role)
            except nextcord.errors.Forbidden:
                pass

@client.command(
    name="archive",
    pass_context=True,
)
async def archive_cmd(ctx):
    await ctx.message.delete()

    date = ctx.message.channel.name.split("-", 1)[1]
    os.makedirs("images" + os.sep + date, exist_ok=True)

    async for log in ctx.message.channel.history(limit=999999):
        if log.attachments:
            for attachment in log.attachments:
                await attachment.save("images" + os.sep + date + os.sep + attachment.filename)

    category = nextcord.utils.get(ctx.guild.categories, name=config["category_archived"])
    if not category:
        category = await ctx.guild.create_category_channel(config["category_archived"])

    await ctx.message.channel.edit(category=category)

    participants = [x for x in ctx.guild.members if config["role_next_rando"] in [role.name for role in x.roles]]

    for participant in participants:
        role = nextcord.utils.get(participant.guild.roles, name=config["role_next_rando"])
        await participant.remove_roles(role)

@client.command(
    name="participant",
    aliases=["participants", "randonneurs", "randonneur"],
    pass_context=True,
)
async def participant_cmd(ctx):
    await ctx.message.delete()

    participants = [x for x in ctx.guild.members if config["role_next_rando"] in [role.name for role in x.roles]]

    embed = nextcord.Embed(color=0x14F5F5)
    embed.title = "Liste des participants"
    if participants:
        embed.description = "- " + "\n- ".join([member.name for member in participants])
    else:
        embed.description = "Aucun participants"
    embed.set_footer(text="By RandoBot")
    await ctx.send(embed=embed)

@client.command(
    name="template",
    pass_context=True,
)
async def template_cmd(ctx):
    await ctx.message.delete()

    await ctx.send("""
@.everyone Rando de la semaine!
- Date : {date}
- Lieu : {lieu}
- RDV : {heure} sur place
- Parking : https://goo.gl/maps/ {parking}
- Repas : Préparer un repas à emporter / sandwich
- Covoiturage : {covoiturage} ({x} places libres)
- Difficulté prévue : {difficulté}

Merci de réagir aux réactions ci-dessous, même si vous ne participez pas.
""")

client.run(os.environ.get("TOKEN"))
