import asyncio
from . import viva_real
from . import imovel_web

async def scrape():
		tasks = [
				viva_real.scrape_page(),
				imovel_web.scrape_page()
		]

		results = await asyncio.gather(*tasks, return_exceptions=True)

		clean = []
		for r in results:
				if isinstance(r, Exception):
						print("Scraper error:", r)
				else:
						clean.append(r)

		results = [item for sublist in clean for item in sublist if sublist is not None]
		return results