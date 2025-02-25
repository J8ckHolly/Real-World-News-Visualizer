from core_db_component import DatabaseCoreComponent
import logging
"""
Filename: table_creation.py

Author: Jack Holly

Date Created: 2025-01-24

Purpose:
    -Inherits all attributes of the core_db_component class
    -creates all tables for the system
"""
class TableCreation(DatabaseCoreComponent):
    
    def __init__(self):
        super().__init__()
        self.make_tables()
        self.create_tables()
        self.__del__()
        
    def create_tables(self):
        self.create_connection()
        cur = self.conn.cursor()
        try:
            for table in self.Tables:
                cur.execute(table)
            self.conn.commit()
            logging.info("Created Tables")
        except Exception as error:
            logging.error("Error while interacting with the database:", error)
        finally:
            if cur:
                cur.close()
        self.close_connection()

    def make_tables(self):
        createArticleTable = """
        CREATE TABLE IF NOT EXISTS article (
            article_id SERIAL PRIMARY KEY,
            ref text UNIQUE,
            time TIMESTAMP,
            country VARCHAR(255),
            Title TEXT
        );
        """
        createDeadArticleTable = """
        CREATE TABLE dead_article (
            ref text PRIMARY KEY,
            time TIMESTAMP,
            FOREIGN KEY (ref) REFERENCES article(ref) ON DELETE CASCADE
        );
        """
        createPageRankerTable = """
        CREATE TABLE page_ranker (
            pageRanker_article_id INT,                  
            country VARCHAR(255) UNIQUE,     
            standard_deviation FLOAT,        
            FOREIGN KEY (pageRanker_article_id) REFERENCES article (article_id) ON DELETE CASCADE
        );
        """
        
        createRankedEventsTable = """
        CREATE TABLE Ranked_Events (
            article_gpt_id INT,   
            gpt_description TEXT, 
            city VARCHAR(255),
            rank INT,                      
            latitude FLOAT,                
            longitude FLOAT,
            
            -- Define the foreign key constraint
            FOREIGN KEY (article_gpt_id) REFERENCES article (article_id) ON DELETE CASCADE
        );
        """

        createRankedEventsExtentedTable = """
        CREATE TABLE ranked_events_extended (
            article_id INT,                       
            related_countries VARCHAR[] ,            
            country_context TEXT[]                    
        );
        """
        
        self.Tables = [createArticleTable, createDeadArticleTable, createPageRankerTable, 
                       createRankedEventsTable, createRankedEventsExtentedTable]