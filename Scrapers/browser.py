from pyppeteer import launch

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

async def launch_browser():
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

	return browser, page