import asyncio
import json
from pyppeteer import launch

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SITE_URL = 'https://www.vivareal.com.br/venda/parana/curitiba/apartamento_residencial/'

async def main():
		# Launch browser
		try:
			browser = await launch(
					executablePath=CHROME_PATH,
					headless=True,
					args=[
							'--no-sandbox',
							'--disable-setuid-sandbox',
            	'--no-first-run',
							'--disable-extensions',
							'--disable-plugins',
							'--disable-background-networking',
							'--disable-infobars',
            	'--mute-audio',
							'--start-maximized',
					],
					ignoreDefaultArgs=[
							'--enable-automation'
					]
			)

			page = await browser.newPage()

			# Set realistic user agent
			await page.setUserAgent(
					"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
					"AppleWebKit/537.36 (KHTML, like Gecko) "
					"Chrome/120.0.0.0 Safari/537.36"
			)

			# Set viewport to match real screen
			await page.setViewport({'width': 1280, 'height': 800})

			# Remove webdriver flag
			await page.evaluateOnNewDocument('''() => {
					Object.defineProperty(navigator, 'webdriver', {
							get: () => false,
					});
			}''')

			# Optional: mimic Chrome runtime
			await page.evaluateOnNewDocument('''() => {
					window.chrome = {
							runtime: {}
					};
			}''')

			# Navigate to a website
			print(f"Navigating to {SITE_URL}...")
			await page.goto(SITE_URL, {'waitUntil': 'networkidle2'})
			
			print(f"Page loaded...")
			await page.waitFor(3000)

			payload = []

			next_page_element = await page.querySelector("a[class*='pagination'][aria-label='próxima página']")
			if next_page_element:
				page_number = 0
				while await page.evaluate('(el) => el.getAttribute("aria-disabled") === "false"', next_page_element) and page_number <= 10:
					print(f"Extracting data from page {page_number+1}...")
					page_payload = await extract_page_info(page)
					payload.extend(page_payload)

					await next_page_element.click()
					next_page_element = await page.waitForSelector("a[class*='pagination'][aria-label='próxima página']")
					await page.waitFor(2000)
					page_number += 1
			else:
				page_payload = await extract_page_info(page)
				payload.extend(page_payload)

			save_payload(payload)
		except Exception as e:
			print(f"An error occurred: {e}")
		finally:
			print("Scraping completed.")
			await browser.close()

async def extract_page_info(page):
	print("Extracting building links...")
	building_links = await page.querySelectorAll('.listings-wrapper li a')
	print(f"{len(building_links)} buildings on the page.")

	page_payload = []
	for link in building_links:
		building_info = await extract_building_info(page, link)
		page_payload.append(building_info)

	return page_payload

async def extract_building_info(page, link):
		return await page.evaluate("""
				(el) => {
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
								titulo: el.title || null,
								link: el.href || null,
								estado: 'PR',
								cidade: 'Curitiba',
								bairro: bairro,
								rua: rua,
								area: el.querySelector('[data-cy*="Area"]')?.innerText.split('\\n')[1].trim() || null,
								quartos: el.querySelector('[data-cy*="bedroom"]')?.innerText.split('\\n')[1].trim() || null,
								banheiros: el.querySelector('[data-cy*="bathroom"]')?.innerText.split('\\n')[1].trim() || null,
								vagas: el.querySelector('[data-cy*="parking"]')?.innerText.split('\\n')[1].trim() || null,
								preco: el.querySelector('[data-cy*="price"]')?.innerText.split('\\n')[0].trim() ||  null
						};
				}
		""", link)

def save_payload(payload):
	print(f"Saving {len(payload)} records to vivareal_data.json...")
	json_payload = json.dumps(payload, ensure_ascii=False, indent=2)
	with open('vivareal_data.json', 'w', encoding='utf-8') as f:
			f.write(json_payload)

# Run async function
asyncio.run(main())