import psycopg2
from psycopg2 import sql
from InitializeDB import load_db_password
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
        """
        print(f"Title: {entry.title}")
        print(f"Link: {entry.link}")
        print(f"Description: {entry.description}")
        print(f"Published: {entry.published}\n")
        """
    

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
    
    def print_country(self):
        print(self.country)
    
    def connect_to_dB(self):
        try:
            self.connection = psycopg2.connect(host="localhost",
                            dbname="postgres",
                            user="postgres",
                            password= self.POSTGRESQL_PASSWORD,
                            port=5432)
        except psycopg2.Error as e:
            print(f"Error: {e}")
        self.cursor = self.connection.cursor()

    
    def Parse_rSS(self):
        
            #Check to make sure URL Length is not longer than 255
            feed = feedparser.parse(rss_url)

    def add_article():
        pass

    def printCountry(self):
        print(self.country)

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    parse_rss_feed()  # This will only run if this file is executed directly
    