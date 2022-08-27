import nextcord
from nextcord.ext import commands

from cogs.utils import config

class ParticipantsCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="participants",
        description="Affiche les participants à la prochaine rando",
        guild_ids=[380373195473027074, 950693381686837248],
    )
    async def participants_cmd(self, ctx: nextcord.Interaction):
        # Get all participants having the next hike role
        participants = [x for x in ctx.guild.members if config["role_next_rando"] in [role.name for role in x.roles]]

        # Send embed message with the list
        embed = nextcord.Embed(color=0x14F5F5)
        embed.title = "Liste des participants"
        if participants:
            embed.description = "- " + "\n- ".join([member.name for member in participants])
        else:
            embed.description = "Aucun participants"
        embed.set_footer(text="By RandoBot")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ParticipantsCommand(bot))
