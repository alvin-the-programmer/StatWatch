import asyncio
import owapi

order = ['Games', 'Win-Rate', 'K/D-Ratio']

tracked = {
	'BadMannered-11804',
	'Kirazuto-1500',
	'Lunar-1153',
	'Oblivion-1572',
	'NerdyPanda-1923',
	'Captain-12480',
	'Lucario-1888',
	'Michelangelo-11865',
	'Ananas-11617',
	'Spyceh-1223'
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

async def swget(battleTag):
	playerStats = await getPlayerStats(battleTag)
	return await playerString(playerStats)

async def getPlayerStats(battleTag):
	quickStats = await owapi.request(battleTag, 'general')
	compStats = await owapi.request(battleTag, 'competitive')
	if quickStats is None or compStats is None:
		return None
	quickStats = processStats(quickStats)
	compStats = processStats(compStats)
	return {'battleTag': battleTag, 'quick': quickStats, 'comp': compStats}

async def addPlayer(battleTag):
	playerStats = await getPlayerStats(battleTag)
	if playerStats is None:
		return False
	players.append(playerStats)
	return True

async def getSortedLadder(mode, stat):
	sortedPlayers = sorted(players, key=lambda k: k[mode][stat], reverse=True)
	playerStrList = []
	for num, s in enumerate(sortedPlayers):
		playerStr = await playerString(s, num + 1)
		playerStrList.append(playerStr)
	response = '*Ladder Ordered by '+ mode + ' ' + stat + ':*\n\n' + '\n\n'.join(playerStrList)
	return response

async def playerString(stats, num=None):
	name = '__**' + stats['quick']['BattleTag'] + '**__  '
	if num is not None: 
		name = '**' + str(num) + '.** ' + name
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









