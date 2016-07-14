import discord
import asyncio
import stats
import myPwd

client = discord.Client()

@client.event
async def on_ready():
    print('Bot logged in as ' + client.user.name + ' ' + client.user.id + '.')

@client.event
async def on_message(message):
    if message.content.startswith('!swget'):
        print('getting!')
        args = message.content.split(' ')
        if len(args) != 2:
            response = 'to get player stats use: \'!swget <BattleTag>\', for example: \'!statWatch Surefour-2559\''
            await client.send_message(message.channel, response)
            return
        tmp = await client.send_message(message.channel, '*Retrieving ' + args[1] + '\'s stats...*')
        response = await stats.getStats(args[1])
        await client.edit_message(tmp, response)
    elif message.content.startswith('!swadd'):
        print('adding!')
        args = message.content.split(' ')
        if len(args) != 2:
            response = 'to add player to leaderboard use: \'!swadd <BattleTag>\', for example: \'!swadd Surefour-2559\''
            await client.send_message(message.channel, response)
            return
        tmp = await client.send_message(message.channel, '*Retrieving ' + args[1] + '\'s stats...*')
        if await stats.addPlayer(args[1]):
            await client.edit_message(tmp, args[1] + ' added to leaderboard.')
        else:
            await client.edit_message(tmp, 'Failed to add ' + args[1] + ' to leaderboard.')
    elif message.content.startswith('!swleaderboard'):
        args = message.content.split(' ')
        response = await stats.getLeaderboard(args[1])
        await client.send_message(message.channel, response)
    elif message.content.startswith('!swfilltest'):
        tmp = await client.send_message(message.channel, 'filling leaderboard with test scrubs...')
        await stats.addTestPlayers()
        await client.edit_message(tmp, 'leaderboard filled.')


client.run('azablan.dev@gmail.com', myPwd.password())
