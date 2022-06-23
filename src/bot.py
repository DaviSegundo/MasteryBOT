import os
import random
from discord.ext import commands
from dotenv import load_dotenv
from utils.lol_api import LoLAPI
from utils.data_formatter import Formatter
from utils.clash_ws import ClashWebScrap
# from database.database import Database


load_dotenv()

# Enviroment variables
TOKEN = os.getenv('DISCORD_TOKEN')
LOL_API_KEY = os.getenv('LOL_API_KEY')
# aws_access_key_id = os.getenv('AWS_PUBLIC')
# aws_secret_access_key = os.getenv('AWS_SECRET')
# region_name = 'sa-east-1'

# Bot instance definition
bot = commands.Bot(command_prefix='&')

# Online objects connection
lol = LoLAPI(LOL_API_KEY)
# database = Database(aws_access_key_id, aws_secret_access_key, region_name)

# Classes builders
formatter = Formatter()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='info', help="Explain how to use all commands.")
async def roll(ctx):
    resp = """```
Bot Commands:

hello: Sends a kind message to the informed person.
    Param:   &hello <name>
    Example: &hello Duduzinho

roll_dice: Simulates rolling dice.
    Param:   &roll_dice <number_of_dices> <number_of_sides>
    Example: &roll_dice 2 20

chest: Inform the champions that you can still get a chest. 
    Param:   &lol chest <lol_name>
    Example: &lol hest BrainLag

clash: Return information about stats of a given player. 
    Param:   &lol clash <lol_name>
    Example: &lol clash BrainLag

name: Return information about avaliable name or not. 
    Param:   &lol name <lol_name>
    Example: &lol name BrainLag
```"""
    await ctx.send(resp)


@bot.command(name='hello')
async def hello(ctx, name: str):
    response = f"Te toma no cu {name}, seu arrombado do krl!!!"
    await ctx.send(response)


@bot.command(name='roll_dice')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='chest')
async def chest(ctx, *args):
    lol_name, out_name = ''.join(args), ' '.join(args)
    player = lol.get_informations_by_name(lol_name)
    if player is not None:
        # information getter
        infos = player.get_no_chest()[:10]
        infos = sorted(infos, key=lambda x: x[2], reverse=True)

        # outputs organization
        output = formatter.format_champions_no_chest(infos, player)

        await ctx.send(f'```{output}```')
    else:
        await ctx.send(f'Name "{out_name}" not found!')


@bot.command(name='clash')
async def clash(ctx, *args):
    lol_name, out_name = ''.join(args), ' '.join(args)
    player = lol.get_informations_by_name(lol_name)
    
    if player is not None:
        ws = ClashWebScrap(lol_name).run()

        # information getter
        mastery_info = player.get_top_mastery()[:5]
        player_info = player.name, player.level
        ranked_info = ws.ranked
        champion_info = ws.champions_infos

        # outputs organization
        output1 = formatter.ranked_info(ranked_info)
        output2 = formatter.champion_info(champion_info)
        output3 = formatter.format_top_mastery(mastery_info)

        out = formatter.format_clash_info(
            player_info, output1, output2, output3)

        await ctx.send(out)
    else:
        await ctx.send(f'Name "{out_name}" not found!')


@bot.command(name='name')
async def clash(ctx, *args):
    lol_name, out_name = ''.join(args), ' '.join(args)
    player = lol.get_informations_by_name(lol_name)
    if player is not None:
        # information getter
        last_game, date_cleanup, days_cleanup, months = player.get_info_cleanup_date()

        # output organization
        out = formatter.format_name_available(
            player.name, player.level, last_game, date_cleanup, days_cleanup, months)

        await ctx.send(out)
    else:
        await ctx.send(f'**{out_name}** is **availabe**!')


if __name__ == '__main__':
    bot.run(TOKEN)
