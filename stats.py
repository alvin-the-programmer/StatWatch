import urllib.request
import json
import asyncio
import aiohttp

order = ['Level', 'Prestige' ,'Rank', 'Games', 'Win-Rate', 'K/D-Ratio']

tracked = {
	'BadMannered-11804',
	'Kirazuto-1500',
	'Lunar-1153',
	'Oblivion-1572',
	'NerdyPanda-1923',
	'Captain-12480',
	'Spyceh-1223',
	'Lucario-1888',
	'Michelangelo-11865'
}

players = []

def statsToString(stats):
	sstats = {k: str(stats[k]) for k in stats}
	statStr = '**' + sstats['BattleTag'] + '**' + '\n'
	for name in order:
		statStr += '***' + name + ':*** ' + sstats[name] + ' **|** '
	statStr = statStr[:-6]
	return statStr

def processStats(stats):
	overallStats = stats['overall_stats']
	avgStats = stats['average_stats']
	gameStats = stats['game_stats']
	newStats = {}
	if overallStats['comprank'] is None:
		newStats['Rank'] = 0
	else:
		newStats['Rank'] = overallStats['comprank']
	newStats['Games'] = overallStats['games']
	newStats['Level'] = overallStats['level'] 
	newStats['Prestige'] = overallStats['prestige']
	winRate = round(overallStats['wins'] / (overallStats['wins'] + overallStats['losses']), 3) * 100
	newStats['Win-Rate'] = round(winRate, 1)
	newStats['K/D-Ratio'] = gameStats['kpd']
	newStats['BattleTag'] = stats['battletag']
	statsToString(newStats)
	return newStats

async def apiRequest(battleTag):
	print('requesting ' + battleTag)
	async with aiohttp.get('https://owapi.net/api/v2/u/' + battleTag + '/stats/general') as r:
		if r.status == 200:
			js = await r.json()
			return js
		else:
			return None

async def getStats(battleTag):
	playerStats = await apiRequest(battleTag)
	playerStats = processStats(playerStats)
	return statsToString(playerStats)

async def addPlayer(battleTag):
	playerStats = await apiRequest(battleTag)
	if playerStats is None:
		return False
	playerStats = processStats(playerStats)
	players.append(playerStats)
	return True

async def getLeaderboard(order):
	sortedPlayers = sorted(players, key=lambda k: k[order], reverse=True)
	statStrs = [statsToString(s) for s in sortedPlayers]
	for i in range(0, len(statStrs)):
		statStrs[i] = '**' + str(i + 1) +'.** ' + statStrs[i]
	response = '*Ladder Ordered by '+ order + ':*\n\n' + '\n\n'.join(statStrs)
	return response

async def trackPlayer(battleTag):
	tracked.add(battleTag)

async def updateProfiles():
	global players
	players = []
	for player in tracked:
		await addPlayer(player)

async def test():
	print('test!')

async def updateLoop():
	while True:
		print('updating')
		await updateProfiles()
		print('update done')
		await asyncio.sleep(180)









