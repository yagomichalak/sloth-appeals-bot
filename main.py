import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
load_dotenv()

client = commands.Bot(command_prefix='za!', intents=discord.Intents.all(), help_command=None)

@client.event
async def on_ready() -> None:
    """ Tells when the bot is ready to run. """

    print('Bot is online!')

# Loads the cogs
for file_name in os.listdir('./cogs/'):
    if file_name.endswith('.py'):
        client.load_extension(f"cogs.{file_name[:-3]}")

# Runs the bot
client.run(os.getenv('TOKEN'))