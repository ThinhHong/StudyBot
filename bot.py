import configparser
import sys
import discord
from discord.ext import commands

config = configparser.ConfigParser()
try:
    config.read('configbot.ini')

except Exception as e:
        print(f'Could not read configuration file {e}')
        sys.exit()

bot_token = config['botSetting']['botToken']
channel_id = int(config['botSetting']['channelId'])

bot_description = "This bot is designed to help students study in groups"
bot_intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', description=bot_description, intents=bot_intents)


@bot.event
async def on_ready():
    message = "Lets start studying!"
    print(message)
    channel = bot.get_channel(channel_id)
    await channel.send(message)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, How are you?")

bot.run(bot_token)
