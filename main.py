import discord
from discord.ext import commands
import music

cogs = [music]

client = commands.Bot(command_prefix='?', intents=discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)



client.run("ODkxMDEzMzYzMzA2NDkxOTY1.YU4K3A.Navl6X46d9R4GXefNGr6hrnNjkA")


