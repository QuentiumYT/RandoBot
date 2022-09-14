import os, json, dotenv, re
from datetime import date, timedelta

# Load dotenv
dotenv.load_dotenv()

# Get all cogs
cogs = [c.replace(".py", "") for c in os.listdir("cogs") if os.path.isfile(os.path.join("cogs", c))]

# Load config
with open("config.json", "r", encoding="utf-8", errors="ignore") as file:
    config = json.loads(file.read(), strict=False)

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
        # Upcoming saturday date
        delta = timedelta(days=5 - date.today().weekday())
        return date.today() + delta if delta.days > 1 else date.today() + delta + timedelta(days=7)
    elif "dimanche" in text_date:
        # Upcoming sunday date
        delta = timedelta(days=6 - date.today().weekday())
        return date.today() + delta if delta.days > 1 else date.today() + delta + timedelta(days=7)
    return None
