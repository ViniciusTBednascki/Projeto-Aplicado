from .browser import launch_browser

MAX_PAGES = 5
SOURCE = 'ImovelWeb'
BASE_URL = 'https://www.imovelweb.com.br'

CIDADES = ['Curitiba']
TIPOS = ['Apartamento', 'Casa']
URLS = ['https://www.imovelweb.com.br/apartamentos-venda-curitiba-pr.html', 'https://www.imovelweb.com.br/casas-venda-curitiba-pr.html']

async def scrape_page():
		payload = []

		try:
			browser, page = await launch_browser()

			print("\nImovelWeb scraper started...")

			for cidade in CIDADES:
				for tipo, url in zip(TIPOS, URLS):
					print(f"\nScraping {tipo} in {cidade}...")
					await page.goto(url, {'waitUntil': 'networkidle2'})
					print(f"Page loaded...")
					await page.waitFor(3000)

					next_page_element = await page.querySelector('a[data-qa="PAGING_NEXT"]')
					if next_page_element:
						page_number = 0
						while bool(next_page_element) and page_number < MAX_PAGES:
							print(f"\nExtracting data from page {page_number+1}...")
							page_payload = await extract_page_info(page, cidade, tipo)
							payload.extend(page_payload)

							await next_page_element.click()
							await page.waitFor(2000)
							next_page_element = await page.waitForSelector('a[data-qa="PAGING_NEXT"]')
							await page.waitFor(1000)
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
	building_links = await page.querySelectorAll('[class*="postingCard"][data-id]')

	page_payload = []
	for link in building_links:
		building_info = await extract_building_info(page, link, cidade, tipo)
		page_payload.append(building_info)

	return page_payload

async def extract_building_info(page, link, cidade, tipo):
		return await page.evaluate("""
				(el, cidade, tipo, source, base_url) => {
						const price_el = el.querySelector('[data-qa="POSTING_CARD_PRICE"]');
						price_text = price_el?.innerText.includes('\\n') ? price_el.innerText.split('\\n')[1].trim() : price_el?.innerText.trim();
						
						info_els = el.querySelectorAll('h3[data-qa*="FEATURES"] span')
						regiao_els = el.querySelectorAll("h4")
						
						return {
								link: base_url + el.getAttribute("data-to-posting"),
								fonte: source,
								tipo: tipo,
								estado: 'PR',
								cidade: cidade,
								bairro: regiao_els[1]?.innerText.split(",")[0].trim() || null,
								rua: regiao_els[0]?.innerText.trim() || null,
								area: info_els[0]?.innerText.replace(/\\D+/g, '').trim() || null,
								quartos: info_els[1]?.innerText.replace(/\\D+/g, '').trim() || null,
								banheiros: info_els[2]?.innerText.replace(/\\D+/g, '').trim() || null,
								vagas: info_els[3]?.innerText.replace(/\\D+/g, '').trim() || null,
								preco: price_text ||  null,
								descricao: el.querySelector('h2[data-qa*="DESCRIPTION"]')?.innerText.trim() || null
						};
				}
		""", link, cidade, tipo, SOURCE, BASE_URL)