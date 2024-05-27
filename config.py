import discord
from discord.ext import commands
from dotenv import load_dotenv
import os


load_dotenv()
token = os.getenv("DISCORD_TOKEN")

exts = [
    "cogs.ticket"
]

class Bot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix, intents=intents, **kwargs)

    async def on_ready(self):
        for ext in exts:
            await self.load_extension(ext)
        print("loaded all cogs")

        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands")
        print("Bot is ready.")

if __name__ == "__main__":
    bot = Bot("!",discord.Intents.default())
    bot.run(token)