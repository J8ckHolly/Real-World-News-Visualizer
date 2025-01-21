import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

def load_db_password():
    try:
        file_path = r'.\webscraping\.env'
        load_dotenv(dotenv_path=file_path)
        POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
        if POSTGRESQL_PASSWORD is None:
            raise ValueError("POSTGRESQL_PASSWORD environment variable is not found")
        return POSTGRESQL_PASSWORD
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def initialize_system_tables():
    POSTGRESQL_PASSWORD = load_db_password()

    createArticleTable = """
    CREATE TABLE IF NOT EXISTS article (
        article_id SERIAL PRIMARY KEY,
        url VARCHAR(255) UNIQUE,
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
    Tables = [createArticleTable, createArticleDescriptionTable,  createRankedEventsTable]
    try:
        conn = psycopg2.connect(host="localhost",
                                dbname="postgres",
                                user="postgres",
                                password=POSTGRESQL_PASSWORD, port=5432)
        cur = conn.cursor()
        """
        Cursor initializes tables with the following attributes

        Article:
            Primary Key article_id
            url
            time
            country
        Article_description:
            Foreign Key article_id <= article.article_id
            filtered_text
        PageRanker_Graph:
            Foreign Key country_id <= article.country
            pageRanker Graph
        Ranked_Events:
            Foreign Key article_gpt_id <= article.article_id
            gpt_description
            city
            rank
        """
        for table in Tables:
            cur.execute(table)
            print("Created Table: "+table)
        conn.commit()

        
    except Exception as error:
        print("Error while interacting with the database:", error)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


initialize_system_tables()
