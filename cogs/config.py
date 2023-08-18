import nextcord
from nextcord.ext import commands

from cogs.utils import config

class ConfigCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="config",
        description="Configure les salons des annonces, les roles et les catégories",
    )
    async def config_cmd(
        self,
        ctx: nextcord.Interaction,
        announcement_channel: nextcord.TextChannel,
        next_hike_role: nextcord.Role,
        hike_category: nextcord.CategoryChannel,
        archived_hikes_category: nextcord.CategoryChannel,
    ):
        if ctx.user.guild_permissions.manage_guild:
            data = {
                "_announcement_channel": announcement_channel.name,
                "announcement_channel": announcement_channel.id,
                "_role_next_rando": next_hike_role.name,
                "role_next_rando": next_hike_role.id,
                "_hike_category": hike_category.name,
                "hike_category": hike_category.id,
                "_archived_hikes_category": archived_hikes_category.name,
                "archived_hikes_category": archived_hikes_category.id,
            }

            config.update(ctx.guild_id, data)

            await ctx.send("Configuration mise à jour !", delete_after=5)

def setup(bot):
    bot.add_cog(ConfigCommand(bot))
