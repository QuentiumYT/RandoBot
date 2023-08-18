import nextcord, re
from nextcord.ext import commands

from cogs.utils import config, find_date

class HistoryCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="history",
        description="Affiche l'historique des randonnées",
    )
    async def history_cmd(self, ctx: nextcord.Interaction):
        # Get all hikes from announcement channel
        announcement_channel = nextcord.utils.get(ctx.guild.channels, id=config.get(ctx.guild_id, "announcement_channel"))

        if not announcement_channel:
            return await ctx.send("Le salon d'annonces n'existe pas !")

        history = {}
        async for hike in announcement_channel.history(limit=999999):
            # Message is a hike with 3 reactions status
            if len(hike.reactions) == 3 and isinstance(hike.reactions[0].emoji, (nextcord.Emoji, nextcord.PartialEmoji)):
                # Old hikes without embed written as text
                if hike.content:
                    name = re.findall(r"Lieu\s*: (.+)", hike.content)
                # New hikes with embed generated by the bot
                elif len(hike.embeds) > 0:
                    name = re.findall(r"\*\*Lieu\*\*: (.+)", hike.embeds[0].description)
                else:
                    continue

                date = find_date(hike.content.lower() or hike.embeds[0].description.lower())

                history[hike.id] = {
                    "name": name[0] if name else "Lieu non défini",
                    "date": date.strftime("%d/%m/%Y") if date else "Date non définie",
                    "participants": hike.reactions[0].count - 1,
                }

        # Reverse history to get last hikes first
        history = dict(reversed(list(history.items())))

        # Send embed message with the list
        embed = nextcord.Embed(color=0x14F5F5)
        embed.title = "Liste des randos organisées"
        if history:
            embed.description = "- " + "\n- ".join([f"{x['name']} {x['date']} ({x['participants']} participant(s))" for x in history.values()])
        else:
            embed.description = "Aucun historique pour le moment"
        embed.set_footer(text="By RandoBot")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HistoryCommand(bot))
