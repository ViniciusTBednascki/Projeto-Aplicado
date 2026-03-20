from .browser import launch_browser

MAX_PAGES = 5
SOURCE = 'VivaReal'

CIDADES = ['Curitiba']
TIPOS = ['Apartamento', 'Casa']
URLS = ['https://www.vivareal.com.br/venda/parana/curitiba/apartamento_residencial/', 'https://www.vivareal.com.br/venda/parana/curitiba/casa_residencial/']

async def scrape_page():
		payload = []

		try:
			browser, page = await launch_browser()

			print("\nVivaReal scraper started...")

			for cidade in CIDADES:
				for tipo, url in zip(TIPOS, URLS):
					print(f"\nScraping {tipo} in {cidade}...")
					await page.goto(url, {'waitUntil': 'networkidle2'})
					print(f"Page loaded...")
					await page.waitFor(3000)

					next_page_element = await page.querySelector("a[class*='pagination'][aria-label='próxima página']")
					if next_page_element:
						page_number = 0
						while await page.evaluate('(el) => el.getAttribute("aria-disabled") === "false"', next_page_element) and page_number < MAX_PAGES:
							print(f"\nExtracting data from page {page_number+1}...")
							page_payload = await extract_page_info(page, cidade, tipo)
							payload.extend(page_payload)

							await next_page_element.click()
							next_page_element = await page.waitForSelector("a[class*='pagination'][aria-label='próxima página']")
							await page.waitFor(2000)
							page_number += 1
					else:
						page_payload = await extract_page_info(page, cidade, tipo)
						payload.extend(page_payload)
		except Exception as e:
			print(f"An error occurred: {e}")
		finally:
			print("\nScraping completed.")
			await browser.close()

		return payload

async def extract_page_info(page, cidade, tipo):
	print("Extracting building links...")
	building_links = await page.querySelectorAll('.listings-wrapper li a')

	page_payload = []
	for link in building_links:
		building_info = await extract_building_info(page, link, cidade, tipo)
		page_payload.append(building_info)

	return page_payload

async def extract_building_info(page, link, cidade, tipo):
		return await page.evaluate("""
				(el, cidade, tipo, source) => {
						const title_el = el.querySelector('h2');
						const regiao = title_el?.innerText.split("\\n")[1].trim() || null;
						let bairro, rua = null;
						if(regiao.includes(',')) {
								bairro = regiao.split(',')[0].trim() || null
								rua = title_el.nextElementSibling.innerText.trim() || null
						} else {
							[rua, bairro] = title_el.nextElementSibling.innerText.split(',', 2).map(s => s.trim()) || [null, null];
						}
						
						return {
								link: el.href || null,
								fonte: source,
								tipo: tipo,
								estado: 'PR',
								cidade: cidade,
								bairro: bairro,
								rua: rua,
								area: el.querySelector('[data-cy*="Area"]')?.innerText.split('\\n')[1].replace(/\\D+/g, '').trim() || null,
								quartos: el.querySelector('[data-cy*="bedroom"]')?.innerText.split('\\n')[1].trim() || null,
								banheiros: el.querySelector('[data-cy*="bathroom"]')?.innerText.split('\\n')[1].trim() || null,
								vagas: el.querySelector('[data-cy*="parking"]')?.innerText.split('\\n')[1].trim() || null,
								preco: el.querySelector('[data-cy*="price"]')?.innerText.split('\\n')[0].trim() ||  null,
								descricao: el.title || null,
						};
				}
		""", link, cidade, tipo, SOURCE)