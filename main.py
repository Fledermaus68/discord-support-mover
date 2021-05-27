import discord
from discord.utils import get
import json
import time

supporterId = 379008590125465602

serverteam = []

data = {}

with open('data.json') as json_file:
    data = json.load(json_file)

supportCount = data['support']

bot = discord.Client(intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Erfolgreich gestartet!')
    for serverGroups in data['serverRoles']:
        for member in bot.get_guild(data['guildId']).members:
            for role in member.roles:
                if role.id == serverGroups:
                    serverteam.append(member.id)


@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        if after.channel.id == data['supportWaiting']:  ## Hier muss der Supportwartebereich hin!
            channel = bot.get_channel(846420223691456523)  ## Da wo sich der Supporter gerade befindet
            members = channel.members
            for member2 in members:
                if not member2.id in serverteam:
                    ## Es ist gerade bereits ein Supportfall!
                    print(
                        'Es ist gerade jemand in den Support Wartebereich gejoint! Weil gerade ein Supportgespräch stattfindet wurde er nicht gemoved! Name: ' + member.name)
                    return
            time.sleep(data['sleepTime'])
            await member.move_to(
                channel)  ## Die Person wird in deinen Support Channel gemoved! Supportfall wird hinzugefügt.
            data['support'] = data['support'] + 1
            print("Es wurde gerade " + member.name + " gemoved. Viel Spaß! Das ist dein #{0} Supportfall.".format(
                data['support']))
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile, ensure_ascii=False, indent=4)
                outfile.close()


bot.run(data['token'])
