
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot aktif sebagai {bot.user}")
    await bot.tree.sync()

async def load_cogs():
    await bot.load_extension("cogs.general")
    await bot.load_extension("cogs.music")

bot.loop.create_task(load_cogs())
bot.run(TOKEN)
