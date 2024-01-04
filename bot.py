import configparser
import sys
import discord
from datetime import datetime
import pytz
from discord.ext import commands
from random import randint, seed
from classes import StudyTime

seed(42)

config = configparser.ConfigParser()
try:
    config.read('configbot.ini')

except Exception as e:
        print(f'Could not read configuration file {e}')
        sys.exit()

bot_token = config['botSetting']['botToken']
channel_id = int(config['botSetting']['channelId'])

bot_description = "This bot is designed to help students study in groups"
intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', description=bot_description, intents=intents)

study_session = StudyTime()

studytip1 ="""
        Get a good night’s sleep. However, this doesn’t only mean getting a full 8 hours of sleep before a big test. 
    What matters even more is getting enough sleep for several nights before you do the bulk of your studying.
    """
studytip2 ="Switch up your study environment. A change in scenery can improve both your memory and concentration levels."
studytip3 ="Stick with an environment that works:"
studytip4 = """
        Listen to calming music: 
    You can listen to any music you like, but many agree that classical, instrumental, 
    and lo-fi beats make good background music for studying and can actually help you pay attention to the task at hand. Songs with lyrics can be distracting.
        """
studytip5 = "Eliminate distractions:"
studytip6 = "Snack on smart food:"

studytips= [studytip1,studytip2,studytip3,studytip4,studytip5,studytip6]

@bot.event
async def on_ready():
    message = "Lets start studying!"
    print(message)
    channel = bot.get_channel(channel_id)
    await channel.send(message)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, How are you?")

@bot.command()
async def add(ctx, arg1, arg2):
    total = int(arg1) + int(arg2)
    await ctx.send(total)

@bot.command()
async def tip(ctx):
    value = randint(0,5)
    await ctx.send(studytips[value])

@bot.command()
async def start(ctx):
    if study_session.is_studying == True:
        await ctx.send("Study session has already begun")
        return
    
    study_session.is_studying = True
    study_session.start_time = ctx.message.created_at.timestamp()
    time = datetime.utcfromtimestamp(study_session.start_time).strftime("%H:%M:%S")
    await ctx.send(f"Studying has begun at: {time}")

bot.run(bot_token)
