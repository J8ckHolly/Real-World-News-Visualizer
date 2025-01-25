import psycopg2
from psycopg2 import sql
from dBManagement.BackUp.InitializeDB import load_db_password
import feedparser
CountryName = "us"

rss_url = f"https://news.google.com/rss/search?q={CountryName}"

import feedparser

def parse_rss_feed():
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
        print(f"Link: {entry.link}")
        print(f"Published: {entry.published}\n") #Time
        
    

class RssUrlParser:

    insert_query = """
    INSERT INTO article (url, time, country)
    VALUES (%s, %s, %s)
    ON CONFLICT (url) DO NOTHING  -- Skip if URL already exists
    """
    
    def __init__(self, country):
        self.country = country
        self.rssLink = f"https://news.google.com/rss/search?q={self.country}"
        self.POSTGRESQL_PASSWORD = load_db_password()
        self.connection = None
        self.cursor = None
        self.connect_to_dB()
    
    def Parse_rSS(self):
        
            #Check to make sure URL Length is not longer than 255
            feed = feedparser.parse(rss_url)




if __name__ == "__main__":
    parse_rss_feed()  # This will only run if this file is executed directly
    