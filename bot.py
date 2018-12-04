import sys
import traceback
import discord
from discord.ext import commands
import data
import os

# Token
token = os.environ['token']

description = '''Bienvenidos al póker de Laguna Gris'''

modules = {'poker.partida_cog'}

bot = commands.Bot(command_prefix='!', description=description)


@bot.event
async def on_ready():
    print('Bot starting...')

    print(bot.user.name)
    print(bot.user.id)
    data.server = bot.get_server('406017502401789953')
    await bot.change_presence(game=discord.Game(name='póker!!'))
    print('Loading cogs...')
    if __name__ == '__main__':
        modules_loaded = 0
        for module in modules:
            try:
                bot.load_extension(module)
                print('\t' + module)
                modules_loaded += 1
            except Exception as e:
                traceback.print_exc()
                print('Error loading the extension {module}', file=sys.stderr)
        print(str(modules_loaded) + '/' + str(modules.__len__()) + ' modules loaded')
        print('Systems 100%')
        print(data.server.name)
    print('------')
# Test bot
bot.run(token)
