import discord
from discord.ext.commands import Bot
import platform
import eng_to_ipa as ipa
import random
from os import path
from wordcloud import WordCloud


client = Bot(description="wordcloud generator", command_prefix="!", pm_help=False)

def file_lengthy(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def CountSyllables(word, isName=False):
    vowels = "aeiouy"
    #single syllables in words like bread and lead, but split in names like Breanne and Adreann
    specials = ["ia","ea"] if isName else ["ia"]
    specials_except_end = ["ie","ya","es","ed"]  #seperate syllables unless ending the word
    currentWord = word.lower()
    numVowels = 0
    lastWasVowel = False
    last_letter = ""

    for letter in currentWord:
        if letter in vowels:
            #don't count diphthongs unless special cases
            combo = last_letter+letter
            if lastWasVowel and combo not in specials and combo not in specials_except_end:
                lastWasVowel = True
            else:
                numVowels += 1
                lastWasVowel = True
        else:
            lastWasVowel = False

        last_letter = letter

    #remove es & ed which are usually silent
    if len(currentWord) > 2 and currentWord[-2:] in specials_except_end:
        numVowels -= 1

    #remove silent single e, but not ee since it counted it before and we should be correct
    elif len(currentWord) > 2 and currentWord[-1:] == "e" and currentWord[-2:] != "ee":
        numVowels -= 1

    return numVowels

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name + ' (ID:' + client.user.id + ') | Connected to ' + str(
        len(client.servers)) + ' servers | Connected to ' + str(len(set(client.get_all_members()))) + ' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__,
                                                                               platform.python_version()))
    print('--------')
    print('made by katski')
    return await client.change_presence(game=discord.Game(name='reading'))


@client.event
async def on_message(message):
    syllables = CountSyllables(message.content)
    if (message.author.bot == True):
        return
    if '!wordcloud' in message.content and len(str(message.content)) < 12:
        d = path.dirname(__file__)
        text = open(path.join(d, 'lonesome.txt')).read()
        wordcloud = WordCloud().generate(text)
        wordcloud = WordCloud(max_font_size=50, background_color="white", contour_width=3).generate(text)
        wordcloud.to_file("cloud.png")
        await client.send_file(message.channel, 'cloud.png')
    if '!wordcloud' in message.content and len(str(message.content)) > 12:
        start = int(message.content[11:(message.content.find(':'))])
        end = int(message.content[(message.content.find(':') + 1):len(message.content)])
        d = path.dirname(__file__)
        text = open(path.join(d, 'lonesome.txt')).read()
        text = text.split()
        text = text[start:end]
        text = " ".join(text)
        wordcloud = WordCloud().generate(text)
        wordcloud = WordCloud(max_font_size=50, background_color="white", contour_width=3).generate(text)
        wordcloud.to_file("cloud.png")
        await client.send_file(message.channel, 'cloud.png')
    if "!syllable" in message.content:
        msg = str(message.content)
        syllables = CountSyllables(msg[11:len(msg)])
        await client.send_message(message.channel, syllables)
    if "!ipa" in message.content:
        msg = str(message.content)
        ipa_msg = ipa.convert(str(msg[4:len(msg)]))
        await client.send_message(message.channel, ipa_msg)
    if "!poem" in message.content:
        dict = {'ir': [], 'ð': [], 'bəl': [], 'ɑd': [], 'im': [], 'ju': [],
                    'ou': [], 'əʧ': [], 'es': [], 'ɪt': [], 'ɪd': []}

        filepath = 'lonesome.txt'
        rhymes = []
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                line = line.replace("\n", "")
                line = line.replace(".", "")
                line = line.replace("!", "")
                if CountSyllables(line) < 7:
                    rhymes.append(line)
                line = fp.readline()
            for i in range(0, len(rhymes)):
                new = ipa.convert(rhymes[i])
                if ("ir" == new[-2:]):
                    dict["ir"].append(rhymes[i])
                if ("ɪr" == new[-2:]):
                    dict["ir"].append(rhymes[i])
                if "bəl" == new[-3:]:
                    dict["bəl"].append(rhymes[i])
                if "ð" == new[-1:]:
                    dict["ð"].append(rhymes[i])
                if "ɑd" == new[-2:]:
                    dict["ɑd"].append(rhymes[i])
                if "i" == new[-1:]:
                    dict["im"].append(rhymes[i])
                if "ju" == new[-2:]:
                    dict["ju"].append(rhymes[i])
                if "oʊ" == new[-2:]:
                    dict["ou"].append(rhymes[i])
                if "əʧ" == new[-2:]:
                    dict["əʧ"].append(rhymes[i])
                if "es" == new[-2:]:
                    dict["es"].append(rhymes[i])
                if "ɪt" == new[-2:]:
                    dict["ɪt"].append(rhymes[i])
                if "ɪd" == new[-2:]:
                    dict["ɪd"].append(rhymes[i])
        print(dict)
        rhymea = random.choice(list(dict))
        rhymeb = random.choice(list(dict))

        await client.send_message(message.channel, random.choice(list(dict[rhymeb])))
        await client.send_message(message.channel, random.choice(list(dict[rhymea])))
        await client.send_message(message.channel, random.choice(list(dict[rhymeb])))
        await client.send_message(message.channel, random.choice(list(dict[rhymea])))


client.run('CLIENT-TOKEN')
