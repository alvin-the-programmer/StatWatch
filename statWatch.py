import discord
import asyncio
import stats
import myPwd

client = discord.Client()

params = ['Level', 'Prestige' ,'Rank', 'Games', 'Win-Rate', 'K/D-Ratio']

def checkLadderArg(myArg):
    myArg = myArg.lower()
    argDict = {k.lower(): k for k in params}
    try:
        return argDict[myArg]
    except KeyError:
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

async def swladder(message, args):
    if len(args) > 2:
        response = 'to list ladder: \'!swladder <Optional Parameter>\', for example: \'!swadd\' or \'!swadd rank\''
        await client.send_message(message.channel, response)
        return
    if len(args) == 1:
        arg = 'Rank'
    else:
        arg = checkLadderArg(args[1])
    if arg:
        response = await stats.getLeaderboard(arg)
        await client.send_message(message.channel, response)
    else:
        await client.send_message(message.channel, 'Invalid ladder parameter, use one of the following: ' )
        await client.send_message(message.channel, params)

async def swfill(message, args):
    tmp = await client.send_message(message.channel, '*filling ladder with test scrubs...*')
    await stats.addTestPlayers()
    await client.edit_message(tmp, 'ladder filled.')

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
    elif message.content.startswith('!swfill'):
        await swfill(message, args)

client.run('azablan.dev@gmail.com', myPwd.password())




