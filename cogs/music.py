
from discord.ext import commands
import discord
import asyncio
import yt_dlp

queues = {}
loop_status = {}

def get_queue(guild_id):
    if guild_id not in queues:
        queues[guild_id] = asyncio.Queue()
    return queues[guild_id]

def get_loop(guild_id):
    return loop_status.get(guild_id, False)

def set_loop(guild_id, value):
    loop_status[guild_id] = value

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_clients = {}

    @commands.hybrid_command(name="play", description="▶️ Putar lagu dari YouTube")
    async def play(self, ctx, *, query: str):
        if ctx.author.voice is None:
            return await ctx.send("❌ Kamu harus join voice channel dulu!")

        vc = ctx.author.voice.channel
        if ctx.voice_client is None:
            await vc.connect()

        ydl_opts = {'format': 'bestaudio', 'noplaylist': 'True'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            url = info['url']
            title = info.get('title', '🎶 Lagu')

        await get_queue(ctx.guild.id).put((url, title))
        await ctx.send(f"🎧 Ditambahkan ke antrean: **{title}**")

        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    async def play_next(self, ctx):
        queue = get_queue(ctx.guild.id)
        vc = ctx.voice_client

        while not queue.empty():
            url, title = await queue.get()
            set_loop(ctx.guild.id, False)

            source = await discord.FFmpegOpusAudio.from_probe(url, method='fallback')
            vc.play(source, after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))
            await ctx.send(f"▶️ Sekarang memutar: **{title}**")
            break

    @commands.hybrid_command(name="skip", description="⏭️ Melewati lagu")
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏭️ Lagu dilewati!")

    @commands.hybrid_command(name="pause", description="⏸️ Menjeda lagu")
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Lagu dijeda.")

    @commands.hybrid_command(name="resume", description="▶️ Melanjutkan lagu")
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Lagu dilanjutkan.")

    @commands.hybrid_command(name="stop", description="⏹️ Menghentikan musik")
    async def stop(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("⏹️ Musik dihentikan dan bot keluar.")

    @commands.hybrid_command(name="queue", description="📜 Lihat antrean lagu")
    async def queue_command(self, ctx):
        q = get_queue(ctx.guild.id)
        if q.empty():
            await ctx.send("📭 Antrean kosong.")
        else:
            msg = "\n".join([f"{i+1}. {item[1]}" for i, item in enumerate(list(q._queue))])
            await ctx.send(f"📜 Antrean lagu:\n{msg}")

    @commands.hybrid_command(name="loop", description="🔁 Aktifkan/Nonaktifkan loop")
    async def loop(self, ctx):
        looping = not get_loop(ctx.guild.id)
        set_loop(ctx.guild.id, looping)
        await ctx.send("🔁 Loop diaktifkan." if looping else "🔁 Loop dimatikan.")

    @commands.hybrid_command(name="volume", description="🔊 Atur volume musik")
    async def volume(self, ctx, volume: int):
        if ctx.voice_client and ctx.voice_client.source:
            ctx.voice_client.source.volume = volume / 100
            await ctx.send(f"🔊 Volume diatur ke {volume}%")

async def setup(bot):
    await bot.add_cog(Music(bot))
