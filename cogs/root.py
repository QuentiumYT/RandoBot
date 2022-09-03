import nextcord, inspect
from subprocess import check_output
# Modules available to execute os commands
import os, psutil
from nextcord.ext import commands

class EvalCode(nextcord.ui.Modal):
    def __init__(self, bot: commands.Bot):
        super().__init__(
            "Évaluer du code",
        )

        self.bot = bot

        self.code = nextcord.ui.TextInput(
            label="Code à évaluer",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="len(bot.guilds)",
            required=True,
        )
        self.add_item(self.code)

    async def callback(self, interaction: nextcord.Interaction):
        code = self.code.value
        bot = self.bot

        if "print(" in code:
            code = "".join(code.replace("print(", "").rsplit(")", 1))
        elif "say(" in code:
            code = "".join(code.replace("say(", "").rsplit(")", 1))

        try:
            # Evaluates the args
            res = eval(code)
            # Await the command
            if inspect.isawaitable(res):
                await res
                awaited = True
            # Send the simple message
            else:
                output = res
                awaited = False
        except Exception as e:
            return await interaction.response.send_message(f'```py\n{e.__class__.__name__}: {e}\n```', ephemeral=True)

        if output is None:
            output = "Code exécuté !"

        elif os.environ.get("TOKEN") in str(output):
            output = "Je ne peux pas divulguer mon token !"

        embed = nextcord.Embed(
            title="Code évalué :",
            color=nextcord.Color.green(),
        )

        if len(str(output)) > 1024:
            with open("output.txt", "w") as file:
                file.write(repr(output))
            file = nextcord.File("output.txt")
            embed.add_field(
                name="Résultat :",
                value="Le résultat est trop long, il est donc disponible dans le fichier ci-dessous.",
            )
            await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
            os.remove("output.txt")
        else:
            embed.add_field(name="Instruction entrée", value=f"```py\n{code}\n```", inline=False)

            embed.add_field(name="Résultat renvoyé", value=f"```py\n{output}\n```", inline=False)

            embed.add_field(name="Synchro", value=f"{awaited}", inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)



class ExecCode(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Exécuter une commande",
        )

        self.command = nextcord.ui.TextInput(
            label="Commande à exécuter",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="",
            required=True,
        )
        self.add_item(self.command)

    async def callback(self, interaction: nextcord.Interaction):
        command = self.command.value

        try:
            # Execute the command and send the result
            output = check_output(command,
                                  shell=True,
                                  stderr=-2) # -2 is equal to STDOUT
        except Exception as e:
            return await interaction.response.send_message(f'```py\n{e.__class__.__name__}: {e}\n```', ephemeral=True)

        if output is None:
            output = "Commande exécutée !"

        elif os.environ.get("TOKEN") in str(output):
            output = "Je ne peux pas divulguer mon token !"

        embed = nextcord.Embed(
            title="Code exécuté :",
            color=nextcord.Color.green(),
        )

        if len(str(output)) > 1024:
            with open("output.txt", "w") as file:
                file.write(repr(output))
            file = nextcord.File("output.txt")
            embed.add_field(
                name="Résultat :",
                value="Le résultat est trop long, il est donc disponible dans le fichier ci-dessous.",
            )
            await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
            os.remove("output.txt")
        else:
            try:
                output = output.decode("utf-8")
            except:
                output = output.decode("iso-8859-1")

            embed.add_field(name="Instruction entrée", value=f"```bash\n{command}\n```", inline=False)

            embed.add_field(name="Résultat renvoyé", value=f"```autohotkey\n{output}\n```", inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)



class RootCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="eval",
        description="Évalue du code Python",
    )
    @commands.is_owner()
    async def eval_cmd(self, ctx: nextcord.Interaction):
        eval_modal = EvalCode(self.bot)
        await ctx.response.send_modal(eval_modal)

    @nextcord.slash_command(
        name="exec",
        description="Exécute des commandes shell",
    )
    @commands.is_owner()
    async def exec_cmd(self, ctx: nextcord.Interaction):
        exec_modal = ExecCode()
        await ctx.response.send_modal(exec_modal)

def setup(bot):
    bot.add_cog(RootCommands(bot))
