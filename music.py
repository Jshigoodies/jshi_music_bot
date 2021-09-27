import discord
from discord.ext import commands
import youtube_dl
import ffmpeg
import asyncio

queue = []


class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = queue

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Join a Voice Channel")

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, url):
        try:
            ctx.voice_client.stop()
        except AttributeError:
            print("here")

        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        YDL_OPTIONS = {'format': "bestaudio"}

        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)

            vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("paused :D")

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send("resumed :D")

    # ------------------------
    @commands.command()
    async def queue(self, ctx, url):
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        YDL_OPTIONS = {'format': "bestaudio"}

        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)

            queue.append(source)

        await ctx.send("added to queue")

    @commands.command()
    async def playqueue(self, ctx): # starting point

        ctx.voice_client.play(queue[0], after=lambda x=None: self.play_next(ctx))

    @commands.command()
    async def clear(self, ctx):
        self.cleared()

    def cleared(self):
        self.queue.clear()

    def play_next(self, ctx): # keeps going until empty
        if len(queue) != 0:
            voice = ctx.guild.voice_client
            queue.pop(0)
            voice.play(queue[0], after=lambda x=None: self.play_next(ctx))
        
    # -------------------------


def setup(client):
    client.add_cog(music(client))
