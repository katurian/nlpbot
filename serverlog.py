from discord.ext.commands import Bot
import discord
import aiofiles
import arrow
from time import gmtime, strftime

client = Bot(command_prefix='!', pm_help=False)

@client.event
async def on_message(message):
    m = await aiofiles.open(f'{"lonesome"}.txt', 'a')
    await m.write(str(message.content) + "\n")
    await m.close()

@client.event
async def on_ready():
    print('Ready to rumble.')

client.run('scottycarma@gmail.com', 'password')
