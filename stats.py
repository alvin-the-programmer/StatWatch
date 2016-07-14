import urllib.request
import json
import asyncio

order = ['Level', 'Rank', 'Games', 'Win-Rate', 'K/D-Ratio']

players = []

def statsToString(stats):
	statStr = '**' + stats['BattleTag'] + '**' + '\n'
	for name in order:
		statStr += '***' + name + ':*** ' + stats[name] + ' **|** '
	statStr = statStr[:-6]
	return statStr

def processStats(stats):
	overallStats = stats['overall_stats']
	avgStats = stats['average_stats']
	gameStats = stats['game_stats']
	newStats = {}
	newStats['Rank'] = str(overallStats['comprank'])
	newStats['Games'] = str(overallStats['games'])
	newStats['Level'] = str(overallStats['prestige']) + '-' +str(overallStats['level'])
	winRate = round(overallStats['wins'] / (overallStats['wins'] + overallStats['losses']), 3) * 100
	newStats['Win-Rate'] = str(round(winRate, 1)) + '%'
	newStats['K/D-Ratio'] = str(gameStats['kpd'])
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
	print(players)
	return True

async def getLeaderboard():
	statStrs = [statsToString(s) for s in players]
	for i in range(0, len(statStrs)):
		statStrs[i] = '**' + str(i + 1) +'.** ' + statStrs[i]
	print(statStrs)
	return '\n\n'.join(statStrs)

