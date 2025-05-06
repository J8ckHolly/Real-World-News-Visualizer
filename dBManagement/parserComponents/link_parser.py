from dataBaseComponents.core_db_component import DatabaseCoreComponent
import datetime
from datetime import datetime
import feedparser
import re
from urllib.parse import quote_plus
import logging

"""
Filename: table_creation.py

Author: Jack Holly

Date Created: 2025-01-24

Purpose:
    -Inherits all attributes of the core_db_component class
    -Gets a request from Google Rss
    -parses rss feed for a given country
    -Commits the country, link, and date to the database
"""
class RssParser(DatabaseCoreComponent):
    def __init__(self, country, dev=False):
        super().__init__()
        if dev == True:
            self.dev = dev
            print("In Developer Mode")
        self.country = country
        self.rss_link = f"https://news.google.com/rss/search?q={quote_plus(self.country)}"
        self.get_rss()
        logging.info(f"{self.country} Parser Created Successfully")
        self.insert_links()

    def get_rss(self):
        self.feed = feedparser.parse(self.rss_link)
    
    def print_time(self):
        print(self.feed.entries[0].published)
    
    def convert_to_timestamp(self,time_published):
        return datetime.strptime(time_published, "%a, %d %b %Y %H:%M:%S GMT")
    
    def insert_links(self):
        insert_tuple = """
            INSERT INTO article (ref, time, country, Title)
            VALUES (%s, %s, %s, %s)
        """
        check_existence = """
            SELECT 1 FROM article WHERE ref = %s
            UNION
            SELECT 1 FROM dead_article WHERE ref = %s
        """


        self.create_connection()
        cur = self.conn.cursor()
        try:
            current_time = datetime.now()

            for entry in self.feed.entries:
                ref = entry.link
                cleaned_title = re.sub(r'[^\x00-\x7F]+', '', entry.title)
                hyphen_index = cleaned_title.rfind(' -')
                if hyphen_index != -1:
                    cleaned_title = cleaned_title[:hyphen_index]
                entry_time = self.convert_to_timestamp(entry.published)

                # Skip entries older than 3 days
                if (current_time - entry_time).days > 3:
                    logging.info(f"Skipping old article: ({entry_time})")
                    continue  

                # Check if ref already exists in article or dead_article
                cur.execute(check_existence, (ref, ref))
                if cur.fetchone():
                    logging.info(f"Link blocked in {self.country} Parser - Already Exists")
                    continue  # Skip insertion if ref is already in one of the tables

                # Insert if unique and within the time limit
                cur.execute(insert_tuple, (ref, entry_time, self.country, cleaned_title))
                logging.info(f"Link added in {self.country} Parser")

            self.conn.commit()

        except Exception as error:
            logging.error("Error while interacting with the database:", error)
        finally:
            if cur:
                cur.close()
        self.close_connection()

    def delete_table_data(self):
        delete_data = """
        DELETE FROM article;
        """
        self.create_connection()
        cur = self.conn.cursor()
        try:
            cur.execute(delete_data)
            self.conn.commit()
        except Exception as error:
            logging.error("Error while interacting with the database:", error)
        finally:
            if cur:
                cur.close()
        self.close_connection()



# Example usage (for testing)
if __name__ == "__main__":
    print("Running Locally")
    country = "United States of America"