import configparser
import sys
import discord
from datetime import datetime
from discord.ext import commands, tasks
from random import randint, seed
from classes import StudyTime

seed(42)


#read config file
config = configparser.ConfigParser()
try:
    config.read('configbot.ini')

except Exception as e:
        print(f'Could not read configuration file {e}')
        sys.exit()

bot_token = config['botSetting']['botToken']
channel_id = int(config['botSetting']['channelId'])

bot_description = "This bot is designed to help students study in groups"

#intents are neccesary for a bot to function. They are choosen by a user
#Each attribute in the Intents class documents which events a bot can corresponds to and which caches it enables.
intents = discord.Intents.all()

intents.message_content = True

bot = commands.Bot(command_prefix='!', description=bot_description, intents=intents)

#Creates studytime class with default values
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

#Bot event are premade discord wrappers that cover many events
@bot.event
async def on_ready():
    """ on_ready function is run when discord bot is first used in a server
    """
    message = "Lets start studying!"
    #Creates like to channel using channel Id
    channel = bot.get_channel(channel_id)
    await channel.send(message)


@bot.command()
async def tip(ctx):
    """sends random top from list

    Args:
        ctx: default parameter found in bot.command wrapper. Stores information send from user in channel
    """
    value = randint(0,5)
    await ctx.send(studytips[value])


"Task will excute at start. Studying session will resume after 15 minutes "
@tasks.loop(minutes=study_session.max_time, count=2)
async def study_break(ctx):
    #Ignore first run
    if study_break.current_loop == 0:
        return

    channel = bot.get_channel(channel_id)
    await channel.send(f"Please take a break for {study_session.break_time} min. Memory retention drops after long study periods")
    resume_study.start(ctx)
        

@tasks.loop(minutes=study_session.break_time, count=2)
async def resume_study(ctx):
    """Sends message to user to return to studying

    Args:
        ctx 
    """
    #Ignore first run
    if resume_study.current_loop == 0:
        return
    
    channel = bot.get_channel(channel_id)
    await channel.send("The break is over. Time to go back to studying :(")

@bot.command()
async def start(ctx):
    """Starts studying session and prepares task loop

    Args:
        ctx (_type_): _description_
    """
    if study_session.is_studying == True:
        await ctx.send("Study session has already begun")
        return
    
    study_session.is_studying = True
    study_session.start_time = ctx.message.created_at.timestamp()
    time = datetime.utcfromtimestamp(study_session.start_time).strftime("%H:%M:%S")
    study_break.start(ctx)
    await ctx.send(f"Studying has begun at: {time} UTC")


@bot.command()
async def end(ctx):
    """ends study session

    Args:
        ctx (_type_): _description_
    """
    if study_session.is_studying == False:
        await ctx.send("Session is not underway")
        return
    
    study_session.is_studying = False
    end_time = ctx.message.created_at.timestamp()
    readable_end = datetime.utcfromtimestamp(end_time).strftime("%H:%M:%S")
    delta = end_time - study_session.start_time
    time = datetime.utcfromtimestamp(delta).strftime("%H:%M:%S")
    study_break.stop()
    await ctx.send(f"Studying session has lasted: {time} and finished at {readable_end}")

bot.run(bot_token)
