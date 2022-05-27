import os
import random
import pandas as pd
import dataframe_image as dfi
import discord
from discord.ext import commands
from dotenv import load_dotenv
from lol import LoLAPI

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
LOL_API_KEY = os.getenv('LOL_API_KEY')

bot = commands.Bot(command_prefix='&')
lol = LoLAPI(LOL_API_KEY)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='info', help="Explain how to use all commands.")
async def roll(ctx):
    resp = """
Bot Commands:

**hello**: Sends a kind message to the informed person.
    **Param**:   $hello <name>
    **Example**: $hello Duduzinho

**roll_dice**: Simulates rolling dice.
    **Param**:   $roll_dice <number_of_dices> <number_of_sides>
    **Example**: $roll_dice 2 20

**mastery**: Inform the champions that you can still get a chest. 
    **Param**:   $mastery <lol_name>  |  __OBS: Dont use spaces in the name.__
    **Example**: $mastery BrainLag
"""
    await ctx.send(resp)

@bot.command(name='hello')
async def nine_nine(ctx, name:str):
    response = f"Te toma no cu {name}, seu arrombado do krl!!!"
    await ctx.send(response)

@bot.command(name='roll_dice')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='mastery')
async def roll(ctx, lol_name: str):
    infos = lol.get_id(lol_name).get_mastery()[:10]
    infos = sorted(infos, key=lambda x: x["points"], reverse=True)
    df = pd.DataFrame(infos)
    df = df.rename(columns={"name": "Champion", "mastery": "Mastery", "points": "Points"})

    dfi.export(df, f'../imgs/{lol_name}.png')
    with open(f'../imgs/{lol_name}.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)
    os.remove(f'../imgs/{lol_name}.png')



bot.run(TOKEN)