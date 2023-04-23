import nextcord, os
from nextcord.ext import commands

from cogs.utils import config

class ArchiveCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="archive",
        description="Archive un salon de rando",
    )
    async def archive_cmd(self, ctx: nextcord.Interaction):
        # Create local folder to store pictures in the channel
        date = ctx.channel.name.split("-", 1)[1]
        os.makedirs("images" + os.sep + date, exist_ok=True)

        # Save all images to the local folder
        async for log in ctx.channel.history(limit=999999):
            if log.attachments:
                for attachment in log.attachments:
                    await attachment.save("images" + os.sep + date + os.sep + attachment.filename)

        # Get archived category and create it if it doesn't exist
        category = nextcord.utils.get(ctx.guild.categories, name=config.get(ctx.guild_id, "category_archived"))
        if not category:
            category = await ctx.guild.create_category_channel(config.get(ctx.guild_id, "category_archived"))

        # Move channel to archived category
        await ctx.channel.edit(category=category)

        # Remove next hike role from all users
        participants = [x for x in ctx.guild.members if config.get(ctx.guild_id, "role_next_rando") in [role.name for role in x.roles]]

        for participant in participants:
            role = nextcord.utils.get(participant.guild.roles, name=config.get(ctx.guild_id, "role_next_rando"))
            await participant.remove_roles(role)

        await ctx.send("Salon rando archivé", delete_after=60)

def setup(bot):
    bot.add_cog(ArchiveCommand(bot))
