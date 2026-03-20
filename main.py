import asyncio
from Scrapers.main import scrape
from databases.mongodb.controller import MongoDBController

MONGODB_COLLECTION = "imoveis"

async def main():
		data = await scrape()

		print(f"Scraped {len(data)} records")

		save_in_mongodb(data)
		# save_in_json(data)

def save_in_mongodb(payload):
		controller = MongoDBController()
		result = controller.bulk_insert(MONGODB_COLLECTION, payload)
		print(f"Inserted {result['inserted']} documents with {result['errors']} errors.")

		controller.close()

def save_in_json(payload):
		import json
		with open('imoveis.json', 'w', encoding='utf-8') as f:
				json.dump(payload, f, ensure_ascii=False, indent=4)
		print("Data saved to imoveis.json")

asyncio.run(main())