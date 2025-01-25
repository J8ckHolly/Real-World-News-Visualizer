from core_db_component import DatabaseCoreComponent
import datetime
from datetime import datetime
import feedparser

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
    def __init__(self, country):
        super().__init__()
        self.country = country
        self.rss_link = f"https://news.google.com/rss/search?q={self.country}"
        self.get_rss()
        print("Created Successfully")

    def get_rss(self):
        self.feed = feedparser.parse(self.rss_link)
    
    def print_time(self):
        print(self.feed.entries[0].published)
    
    def convert_to_timestamp(self,time_published):
        return datetime.strptime(time_published, "%a, %d %b %Y %H:%M:%S GMT")
    
    def insert_entry(self):
        insert_tuple = """
            INSERT INTO article (link, time, country)
            VALUES (%s, %s, %s)
        """
        check_article_table = """
            SELECT 1 FROM article WHERE link = %s AND country = %s
        """

        check_duplicate_table = """
            SELECT 1 FROM Duplicate_Table WHERE link = %s AND country = %s
        """

        self.create_connection()
        cur = self.conn.cursor()
        try:
            current_time = datetime.now()

            for entry in self.feed.entries:
                entry_time = self.convert_to_timestamp(entry.published)

                if (current_time - entry_time).days > 3:
                    continue  # Skip this entry as it's older than 3 days. Also check back later for GMT Conversion

                cur.execute(check_article_table, (entry.link, self.country))
                if cur.fetchone():
                    continue  # Skip if link-country combination already exists in 'article'
                
                # Check if the link and country combination already exists in 'duplicate_article'
                cur.execute(check_duplicate_table, (entry.link, self.country))
                if cur.fetchone():
                    continue  # Skip if link-country combination already exists in 'duplicate_article'

                cur.execute(insert_tuple, (entry.link, 
                            self.convert_to_timestamp(entry.published),
                            self.country))
            self.conn.commit()

        except Exception as error:
            print("Error while interacting with the database:", error)
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
            print("Error while interacting with the database:", error)
        finally:
            if cur:
                cur.close()
        self.close_connection()



    