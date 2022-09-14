import nextcord

class SelectDifficulty(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="Chill (5km)", emoji="😄"),
            nextcord.SelectOption(label="Normal (8km)", emoji="😊"),
            nextcord.SelectOption(label="Difficile (12km)", emoji="😬"),
            nextcord.SelectOption(label="Hardcore (+15km)", emoji="🥵"),
        ]

        super().__init__(
            placeholder="Difficulté de la rando",
            max_values=2,
            min_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction):
        embed = interaction.message.embeds[0]

        embed.description += f"\n**Difficulté:** {' / '.join(list(self.values))}"

        await interaction.message.edit(embed=embed, view=SelectSeatsView())

class SelectDifficultyView(nextcord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(SelectDifficulty())



class SelectSeats(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="A voir mais voiture dispo", emoji="🚗"),
            nextcord.SelectOption(label="Yes, 4 places perso", emoji="4️⃣"),
            nextcord.SelectOption(label="Yes, 3 places perso", emoji="3️⃣"),
            nextcord.SelectOption(label="Yes, 2 places perso", emoji="2️⃣"),
            nextcord.SelectOption(label="Yes, 1 place perso", emoji="1️⃣"),
            nextcord.SelectOption(label="Pas de voiture perso :/", emoji="❌"),
        ]

        super().__init__(
            placeholder="Covoiturage",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction):
        embed = interaction.message.embeds[0]

        embed.description += f"\n**Covoiturage:** {self.values[0]}"

        await interaction.message.edit(embed=embed, view=SelectCarShareView())

class SelectSeatsView(nextcord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(SelectSeats())



class SelectCarShare(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="Repas de midi", emoji="🍴"),
            nextcord.SelectOption(label="Goûter", emoji="🍪"),
            nextcord.SelectOption(label="Repas du soir !?", emoji="🍕"),
            nextcord.SelectOption(label="Pas de repas requis", emoji="❌"),
            nextcord.SelectOption(label="A voir en fonction du RDV", emoji="🤷"),
        ]

        super().__init__(
            placeholder="Repas à emmener",
            min_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction):
        embed = interaction.message.embeds[0]

        embed.description += f"\n**Repas:** {self.values[0]}"

        await interaction.message.edit(view=None, embed=embed)

class SelectCarShareView(nextcord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(SelectCarShare())
