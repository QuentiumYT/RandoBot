import os, json, dotenv

# Load dotenv
dotenv.load_dotenv()

# Get all cogs
cogs = [c.replace(".py", "") for c in os.listdir("cogs") if os.path.isfile(os.path.join("cogs", c))]

# Load config
with open("config.json", "r", encoding="utf-8", errors="ignore") as file:
    config = json.loads(file.read(), strict=False)
