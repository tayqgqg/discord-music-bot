
from discord.ext import commands
import discord

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send("👋 Halo! Aku adalah bot serba bisa!")

    @commands.hybrid_command(name="help", with_app_command=True, description="📚 Tampilkan semua perintah")
    async def help_command(self, ctx):
        embed = discord.Embed(title="📚 Daftar Perintah", color=discord.Color.blurple())
        embed.add_field(name="👋 !hello", value="Menyapa bot", inline=False)
        embed.add_field(name="🎲 !roll", value="Roll angka acak", inline=False)
        embed.add_field(name="📅 !remind", value="Buat pengingat", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
