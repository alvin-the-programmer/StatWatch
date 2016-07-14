import urllib.request
import json
import asyncio

order = ['Level', 'Prestige' ,'Rank', 'Games', 'Win-Rate', 'K/D-Ratio']

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
	url = 'https://owapi.net/api/v2/u/' + battleTag + '/stats/general'
	try:
		data = urllib.request.urlopen(url).read()
		data = data.decode('utf-8')
		return json.loads(data)
	except urllib.error.HTTPError:
		print('request failed')
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
	return '\n\n'.join(statStrs)

async def addTestPlayers():
	await addPlayer('BadMannered-11804')
	await addPlayer('Kirazuto-1500')
	await addPlayer('Lucario-1888')
	await addPlayer('Lunar-1153')
	await addPlayer('Oblivion-1572')
	await addPlayer('Michelangelo-11865')
	await addPlayer('Demetri-1640')
	# await addPlayer('NerdyPanda-1923')
	# await addPlayer('Captain-12480')
	# await addPlayer('Spyceh-1223')











