import os, json, dotenv, re
from datetime import date, timedelta

# Load dotenv
dotenv.load_dotenv()

# Get all cogs
cogs = [c.replace(".py", "") for c in os.listdir("cogs") if os.path.isfile(os.path.join("cogs", c))]

# Handle config
class Config:
    def __init__(self, file: str = "config.json"):
        self.file = file
        self.load()

    def __getitem__(self, key):
        return self.config.get(key)

    def __setitem__(self, key, value):
        self.config[key] = value

    def load(self):
        if os.path.isfile("data/" + self.file):
            with open("data/" + self.file, "r", encoding="utf-8", errors="ignore") as file:
                self.config = json.loads(file.read())
        else:
            self.config = {}

        return self.config

    def save(self):
        with open("data/" + self.file, "w", encoding="utf-8", errors="ignore") as file:
            file.write(json.dumps(self.config, indent=4, ensure_ascii=False))

    def update(self, guild_id: int, data: dict):
        # Merge both dicts
        self.config[str(guild_id)] = data
        self.save()

    def get(self, guild_id: int, value: str):
        guild_data = self.config.get(str(guild_id))
        return guild_data.get(value)

config = Config()



def find_date(text_date: str) -> date:
    if planned_date := re.findall(r"(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.]((20)?\d{2})", text_date):
        # Specified date
        # Year is a 2 digits number
        if len(planned_date[0][2]) == 2:
            return date(int("20" + planned_date[0][2]), int(planned_date[0][1]), int(planned_date[0][0]))
        # Year is the full number
        else:
            return date(int(planned_date[0][2]), int(planned_date[0][1]), int(planned_date[0][0]))
    elif "demain" in text_date:
        # Tomorrow date
        return date.today() + timedelta(days=1)
    elif "samedi" in text_date:
        # Upcoming Saturday date
        delta = timedelta(days=5 - date.today().weekday())
        return date.today() + delta if delta.days > 1 else date.today() + delta + timedelta(days=7)
    elif "dimanche" in text_date:
        # Upcoming Sunday date
        delta = timedelta(days=6 - date.today().weekday())
        return date.today() + delta if delta.days > 1 else date.today() + delta + timedelta(days=7)
    return None
