import discord
import asyncio
from discord.ext.commands import Bot
import platform
import wordcloud
from os import path
from wordcloud import WordCloud

client = Bot(description = "wordcloud generator", command_prefix = "!", pm_help = False)

@client.event
async def on_ready():
  print('Logged in as ' + client.user.name + ' (ID:' + client.user.id + ') | Connected to ' + str(len(client.servers)) + ' servers | Connected to ' + str(len(set(client.get_all_members()))) + ' users')
  print('--------')
  print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
  print('--------')
  print('made by katski')
  return await client.change_presence(game = discord.Game(name = 'reading'))

@client.event
async def on_message(message):
  if (message.author.bot == True):
    return
  if '!wordcloud' in message.content and len(str(message.content)) < 12:
    d = path.dirname(__file__)
    text = open(path.join(d, 'lonesome.txt')).read()
    wordcloud = WordCloud().generate(text)
    wordcloud = WordCloud(max_font_size = 50, background_color = "white", contour_width = 3).generate(text)
    wordcloud.to_file("cloud.png")
    await client.send_file(message.channel, 'cloud.png')
  if '!wordcloud' in message.content and len(str(message.content)) < 12:
    d = path.dirname(__file__)
    text = open(path.join(d, 'lonesome.txt')).read()
    wordcloud = WordCloud().generate(text)
    wordcloud = WordCloud(max_font_size = 50, background_color = "white", contour_width = 3).generate(text)
    wordcloud.to_file("cloud.png")
    await client.send_file(message.channel, 'cloud.png')



 
client.run('NTY5MDA1ODQ4Njk3ODk2OTgw.XLqWPw.icjkwfrh-3CWh0ZnadfFB53E2RA')
