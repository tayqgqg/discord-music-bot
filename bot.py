import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("cogs.general")
        await self.load_extension("cogs.music")
        await self.tree.sync()  # untuk slash command

bot = MyBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot aktif sebagai {bot.user}")

bot.run(TOKEN)
