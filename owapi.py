import asyncio
import aiohttp

async def request(battleTag, mode):
	url = 'https://owapi.net/api/v2/u/' + battleTag + '/stats/' + mode
	async with aiohttp.get(url) as r:
		if r.status == 200:
			print('request success ' + str(r.status) + ' ' + url)
			js = await r.json()
			return js
		else:
			print('request failed '+ str(r.status) + ' ' + url)
			return None