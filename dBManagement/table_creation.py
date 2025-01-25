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
            link TEXT UNIQUE,
            time TIMESTAMP,
            country VARCHAR(255)
        );
        """
        createArticleDescriptionTable = """
        CREATE TABLE article_description (
            article_id INT,                  -- Foreign key column
            filtered_text TEXT,              -- Text field to store filtered description
            
            -- Define the foreign key constraint
            CONSTRAINT fk_article_id FOREIGN KEY (article_id) REFERENCES article (article_id)
        );
        """
        #createPageRankerGraphTable = """
        #CREATE TABLE PageRanker_Graph (
        #    article_country VARCHAR(255),               -- Foreign key to article's country
        #    pageRankerGraph TEXT,         -- This will store the graph, using TEXT or a more suitable type
        #    CONSTRAINT fk_country FOREIGN KEY (article_country) REFERENCES article (country)
        #);
        #"""
        
        createRankedEventsTable = """
        CREATE TABLE Ranked_Events (
            article_gpt_id INT,           -- Foreign key to article_id from the article table
            gpt_description TEXT,         -- Text field for GPT description
            city VARCHAR(255),             -- City field with a maximum length of 255 characters
            rank INT,                      -- Rank field (integer type)
            
            -- Define the foreign key constraint
            CONSTRAINT fk_article_gpt_id FOREIGN KEY (article_gpt_id) REFERENCES article (article_id)
        );
        """

        createDuplicateTable = """
        CREATE TABLE Duplicate_Table (
            link TEXT UNIQUE,
            country VARCHAR(255)
        );
        """
        self.Tables = [createArticleTable, createArticleDescriptionTable,  createRankedEventsTable, createDuplicateTable]





