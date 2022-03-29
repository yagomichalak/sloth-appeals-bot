import discord
from discord.ext import commands, tasks

import os
from dotenv import load_dotenv
load_dotenv()

client = commands.Bot(command_prefix='za!', intents=discord.Intents.all(), help_command=None)

@client.event
async def on_ready() -> None:
    """ Tells when the bot is ready to run. """

    change_status.start()
    print('Bot is online!')

@tasks.loop(minutes=1)
async def change_status() -> None:
    """ Changes the bot's status """

    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening, name=f'appeals on /appeal.')
        )

# Loads the cogs
for file_name in os.listdir('./cogs/'):
    if file_name.endswith('.py'):
        client.load_extension(f"cogs.{file_name[:-3]}")

# Runs the bot
client.run(os.getenv('TOKEN'))