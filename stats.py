import urllib.request
import json
import asyncio
import aiohttp

order = ['Games', 'Win-Rate', 'K/D-Ratio']

tracked = {
	# 'Spyceh-1223',
	'BadMannered-11804',
	'Kirazuto-1500',
	'Lunar-1153',
	'Oblivion-1572',
	'NerdyPanda-1923',
	'Captain-12480',
	'Lucario-1888',
	'Michelangelo-11865',
	'Ananas-11617'
}

players = []

def statsToString(stats):
	sstats = {k: str(stats[k]) for k in stats}
	statStr = ''
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

async def apiRequestQuick(battleTag):
	print('requesting quick-play stats for: ' + battleTag)
	async with aiohttp.get('https://owapi.net/api/v2/u/' + battleTag + '/stats/general') as r:
		if r.status == 200:
			js = await r.json()
			return js
		else:
			print(battleTag + ' quick request failed')
			return None

async def apiRequestComp(battleTag):
	print('requesting competitive-play stats for: ' + battleTag)
	async with aiohttp.get('https://owapi.net/api/v2/u/' + battleTag + '/stats/competitive') as r:
		if r.status == 200:
			js = await r.json()
			return js
		else:
			print(battleTag + ' comp request failed')
			return None

async def getStats(battleTag):
	playerStats = await apiRequest(battleTag)
	playerStats = processStats(playerStats)
	return statsToString(playerStats)

async def addPlayer(battleTag):
	quickStats = await apiRequestQuick(battleTag)
	compStats = await apiRequestComp(battleTag)
	if quickStats is None or compStats is None:
		return False
	quickStats = processStats(quickStats)
	compStats = processStats(compStats)
	players.append({'battleTag': battleTag, 'quick': quickStats, 'comp': compStats})
	return True

async def getSortedLadder(mode, stat):
	sortedPlayers = sorted(players, key=lambda k: k[mode][stat], reverse=True)
	playerStrList = []
	for num, s in enumerate(sortedPlayers):
		playerStr = await playerString(num + 1, s)
		playerStrList.append(playerStr)
	response = '*Ladder Ordered by '+ mode + ' ' + stat + ':*\n\n' + '\n\n'.join(playerStrList)
	return response

async def playerString(num, stats):
	name = '**' + str(num) + '.** ' + '__**' + stats['quick']['BattleTag'] + '**__  '
	rank = 'Rank ' + str(stats['quick']['Rank'])
	prestige = 'Prestige ' + str(stats['quick']['Prestige'])
	level = 'Level ' + str(stats['quick']['Level'])
	header = name + prestige + ' **|** ' + level + ' **|** ' + rank
	quick = '       **Quick:**  ' + statsToString(stats['quick'])
	comp = '       **Comp:**  ' + statsToString(stats['comp'])
	playerStr = header + '\n' + quick + '\n' + comp
	return playerStr

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
		for p in players:
			print(p['quick']['BattleTag'])
		await asyncio.sleep(1200)









