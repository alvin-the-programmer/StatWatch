import discord
import asyncio
import stats
import botLogin

client = discord.Client()

params = ['Level', 'Prestige' ,'Rank', 'Games', 'Win-Rate', 'K/D-Ratio']

def checkStatArg(myArg):
    myArg = myArg.lower()
    argDict = {k.lower(): k for k in params}
    try:
        return argDict[myArg]
    except KeyError:
        return False

def checkModeArg(myArg):
    myArg = myArg.lower()
    if myArg == 'quick' or myArg == 'comp':
        return myArg
    else:
        return False

async def swget(message, args):
    if len(args) != 2:
        response = 'to get player stats use: \'!swget <BattleTag>\', for example: \'!statWatch Surefour-2559\''
        await client.send_message(message.channel, response)
        return
    tmp = await client.send_message(message.channel, '*Retrieving ' + args[1] + '\'s stats...*')
    response = await stats.getStats(args[1])
    await client.edit_message(tmp, response)

async def swadd(message, args):
    if len(args) != 2:
        response = 'to add player to ladder use: \'!swadd <BattleTag>\', for example: \'!swadd Surefour-2559\''
        await client.send_message(message.channel, response)
        return
    tmp = await client.send_message(message.channel, '*Retrieving ' + args[1] + '\'s stats...*')
    if await stats.addPlayer(args[1]):
        await client.edit_message(tmp, args[1] + ' added to ladder.')
    else:
        await client.edit_message(tmp, 'Failed to add ' + args[1] + ' to ladder.')

async def swtrack(message, args):
    tmp = await client.send_message(message.channel, '*Tracking' + args[1] + '\'s stats...*')
    await stats.trackPlayer(args[1])

async def swladder(message, args):
    if len(args) == 1:
        arg1 = 'quick'
        arg2 = 'Win-Rate'
    elif len(args) == 3:
        arg1 = checkModeArg(args[1])
        arg2 = checkStatArg(args[2])
    if arg1 and arg2:
        response = await stats.getSortedLadder(arg1, arg2)
    else:
        response = 'to list ladder list: \'!swladder <mode> <stat>\', for example: \'!swladder\' or \'!swladder quick k/d-ratio\''
    while len(response) > 1400:
        i = response.find('\n\n', 1400)
        await client.send_message(message.channel, response[:i])
        response = response[i + 1:]
    await client.send_message(message.channel, response)

@client.event
async def on_ready():
    print('Bot logged in as ' + client.user.name + ' ' + client.user.id + '.')

@client.event
async def on_message(message):
    args = message.content.split(' ')
    if message.content.startswith('!swget'):
        await swget(message, args)
    elif message.content.startswith('!swadd'):
        await swadd(message, args)
    elif message.content.startswith('!swladder'):
        await swladder(message, args)
    elif message.content.startswith('!swtrack'):
        await swtrack(message, args)
    # elif message.content.startswith('!untrack'):
    elif message.content.startswith('!swupdate'):
        await stats.updateProfiles()
    elif message.content.startswith('!swloop'):
        await stats.updateLoop()

client.run('azablan.dev@gmail.com', 'Philip123')




