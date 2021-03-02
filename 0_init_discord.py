import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '!',description = "daily")

@bot.event
async  def on_ready():
    print("Ready !")

@bot.event
async def on_message(message):
    if message.content.lower() == "ping":
        await message.channel.send('pong', delete_after=5)
bot.run(API)

#https://www.integromat.com/scenario/1878842/edit
