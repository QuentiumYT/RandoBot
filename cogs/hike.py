import nextcord, re
from nextcord.ext import commands
from datetime import date, timedelta

from cogs.utils import config

from cogs.components.hike_selects import SelectDifficultyView

class HikeInfo(nextcord.ui.Modal):
    def __init__(self, bot: commands.Bot):
        super().__init__(
            "Organiser une rando",
            timeout=5 * 60,
        )

        self.bot = bot

        self.description = nextcord.ui.TextInput(
            label="Description / motivation de la rando",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="Proposition de rando, qui serait dispo ?",
            required=True,
            min_length=20,
            max_length=600,
        )
        self.add_item(self.description)

        self.place = nextcord.ui.TextInput(
            label="Lieu",
            placeholder="Col du Donon | Chateau du Wasenbourg",
            required=True,
            min_length=3,
            max_length=200,
        )
        self.add_item(self.place)

        self.date = nextcord.ui.TextInput(
            label="Date",
            placeholder="30/08/2022 | 11/12 | demain | samedi | dimanche",
            required=True,
            min_length=5,
            max_length=10,
        )
        self.add_item(self.date)

        self.time = nextcord.ui.TextInput(
            label="Heure",
            placeholder="10h00 | 13:30",
            default_value="10h00",
            required=True,
            min_length=4,
            max_length=10,
        )
        self.add_item(self.time)

        self.duration = nextcord.ui.TextInput(
            label="Durée",
            placeholder="5h | 10h | 20h (déter!)",
            required=False,
        )
        self.add_item(self.duration)

    async def callback(self, interaction: nextcord.Interaction):
        if planned_date := re.findall(r"(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](20\d{2})", self.date.value):
            # Specified date
            date_obj = date(int(planned_date[0][2]), int(planned_date[0][1]), int(planned_date[0][0]))
        elif "demain" in self.date.value.lower():
            # Tomorrow date
            date_obj = date.today() + timedelta(days=1)
        elif "samedi" in self.date.value.lower():
            # Upcoming saturday date
            delta = timedelta(days=5 - date.today().weekday())
            date_obj = date.today() + delta if delta.days > 1 else date.today() + delta + timedelta(days=7)
        elif "dimanche" in self.date.value.lower():
            # Upcoming sunday date
            delta = timedelta(days=6 - date.today().weekday())
            date_obj = date.today() + delta if delta.days > 1 else date.today() + delta + timedelta(days=7)
        else:
            return await interaction.send("La date est invalide, merci de spécifier une date valide.", delete_after=20)

        date_repr = date_obj.strftime("%d-%m-%Y")

        # Sent embed with all infos
        embed = nextcord.Embed(
            title="Sondage prochaine randonnée",
            description="""
            @everyone {}
            **Lieu**: {}
            **Date**: {}
            **Heure**: {}
            **Durée**: {}
            """.format(
                self.description.value,
                self.place.value,
                date_repr,
                self.time.value,
                self.duration.value or "Non précisée",
            ),
            color=nextcord.Color.green(),
        )
        embed.set_footer(text=f"Rando organisée par {interaction.user.display_name}", icon_url=interaction.user.avatar.url)

        rando_msg = await interaction.response.send_message(embed=embed, view=SelectDifficultyView())

        # Add reactions to the rando message
        rando_msg = await rando_msg.fetch()

        await rando_msg.add_reaction(nextcord.utils.get(self.bot.emojis, name="Check"))
        await rando_msg.add_reaction(nextcord.utils.get(self.bot.emojis, name="Average"))
        await rando_msg.add_reaction(nextcord.utils.get(self.bot.emojis, name="Cross"))

        # Create a new channel with the date of the hike
        category = nextcord.utils.get(rando_msg.guild.categories, name=config["category_default"])

        channel = await rando_msg.guild.create_text_channel("rando-" + date_repr, category=category)

        # Permissions for users in the new channel
        overwrites = {
            rando_msg.guild.default_role: nextcord.PermissionOverwrite(view_channel=True, send_messages=True),
            interaction.user: nextcord.PermissionOverwrite(view_channel=True, send_messages=True, mention_everyone=True),
            nextcord.utils.get(interaction.user.guild.roles, name=config["role_next_rando"]): nextcord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        for target, overwrite in overwrites.items():
            await channel.set_permissions(target, overwrite=overwrite)



class HikeCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="rando",
        description="Organiser une rando",
        guild_ids=[380373195473027074, 950693381686837248],
    )
    async def rando_cmd(self, ctx: nextcord.Interaction):
        info_modal = HikeInfo(self.bot)
        await ctx.response.send_modal(info_modal)

def setup(bot):
    bot.add_cog(HikeCommand(bot))
