import aiohttp
import asyncio

async def request(battleTag, mode):
	url = 'https://owapi.net/api/v2/u/' + battleTag + '/stats/' + mode
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			if response.status == 200:
				print('request success ' + str(response.status) + ' ' + url)
				return await response.json()
			else:
				print('request failed '+ str(response.status) + ' ' + url)
				return None
