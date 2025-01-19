

CountryName = "us"

rss_url = f"https://news.google.com/rss/search?q={CountryName}"

import feedparser


# Parse the RSS feed
feed = feedparser.parse(rss_url)

# Print feed title and description
print(f"Feed Title: {feed.feed.title}")
print(f"Feed Description: {feed.feed.description}")
print(f"Feed Link: {feed.feed.link}")
print("\nItems:")

count = 0
# Loop through each entry (RSS item)
for entry in feed.entries:
    print(f"Link: {entry.published}")
    """
    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Description: {entry.description}")
    print(f"Published: {entry.published}\n")
    """
    

class RssUrlParser:
    
    def __init__(self, country):
        self.country = country
        self.rssLink = f"https://news.google.com/rss/search?q={self.country}"
    
    def printCountry(self):
        print(self.country)

    