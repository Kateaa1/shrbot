# Imports
import logging
import os
import random
from datetime import datetime
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Setting up the tokens
load_dotenv()
discord_token = os.getenv("DISCORD_API_KEY", "")  # Don't leak this lmao

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

# path to images
image_directory = Path(os.getenv("IMAGE_PATH", ""))


def pull_image():
    all_images = [f for f in image_directory.iterdir() if f.is_file]
    chosen_image = random.choice(all_images)
    return chosen_image


# Bot intents stuff (I hate intents)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Logging
logger = logging.FileHandler(filename="shrbot.log", encoding="utf-8", mode="w")

shrbot_role = "shrbcat"

############
## Events ##
############


# Init the bot
@bot.event
async def on_ready():
    print(f"Shrbot is ready {current_time}")


############
# Commands #
############


# Assigns shrbcat role
@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=shrbot_role)
    if role:
        # Adds role to user
        await ctx.author.add_roles(role)
        print(f"assigned {role} to {ctx.author}")
        # Confirms role was added!
        await ctx.send(f"{ctx.author.mention} was just assigned {role}")
    else:
        await ctx.send(f"{ctx.author.mention} Role does not exist!")
        print(f"failed to assign {role} to {ctx.author} {current_time}")


@bot.command()
async def unassign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=shrbot_role)
    if role:
        # Removed role from user
        await ctx.author.remove_roles(role)
        print(f"Removed {role} from {ctx.author}")
        # Confirms role was added!
        await ctx.send(f"{ctx.author.mention} just had {role} removed {current_time}")
    else:
        await ctx.send(f"{ctx.author.mention} Role does not exist!")
        print(f"failed to remove {role} from {ctx.author} {current_time}")


@bot.command()
@commands.has_role(shrbot_role)
# Needs img perms and access to img function
async def sendcat(ctx):
    shrbcat = pull_image()
    await ctx.send(file=discord.File(shrbcat))
    print(f"{shrbcat} sent! {current_time}")


@sendcat.error
async def norole(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(
            f"{ctx.author.mention} to use that command you need the shrbcat role!\nTo get that role use !assign"
        )
        print(f"{ctx.author} is not a shrbcat {current_time}")


# Run the bot
bot.run(discord_token, log_handler=logger, log_level=logging.ERROR)
