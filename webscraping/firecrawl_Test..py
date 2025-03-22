from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv
load_dotenv()

FIRE_CRAWL_API = os.getenv("FIRE_CRAWL_API")

app = FirecrawlApp(api_key=FIRE_CRAWL_API)
exit
response = app.scrape_url(url='https://www.cbsnews.com/news/u-s-to-revoke-legal-status-of-over-a-half-million-migrants-chnv/', params={
	'formats': [ 'markdown' ],
    "onlyMainContent": True
})
print(response)

with open("scraped_content.txt", "w", encoding="utf-8") as file:
    file.write(response.get("markdown", "No content available"))



