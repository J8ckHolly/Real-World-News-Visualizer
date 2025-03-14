import feedparser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PageRankingAlgo import Node, WeightedGraph
from core_db_component import DatabaseCoreComponent
import logging
"""
Filename: table_creation.py

Author: Jack Holly

Date Created: 2025-01-24

Purpose:
    -Inherits all attributes of the core_db_component class
    -Pulls all articles from article table and runs the pageranker algorithm
    -Selects the most relevant article 
    -Need to work on standard deviation
"""
class articleSelector(DatabaseCoreComponent):
    def __init__(self, country):
        super().__init__()
        self.country = country
        self.titles = []
        self.UID = []

    def get_id_title_data(self):
        get_article_data = """
            SELECT article_id, title
            FROM article
            WHERE country = %s
        """
        self.create_connection()
        cur = self.conn.cursor()
        try:
            cur.execute(get_article_data, (self.country,))  # Pass country safely
            rows = cur.fetchall()  # Store the result in self.Articles
            self.UID = {row[0] for row in rows}  # Set of article_id
            self.titles = " ".join(row[1] for row in rows)  # Concatenated titles

        except Exception as error:
            logging.error("Error while interacting with the database:", error)
        finally:
            if cur:
                cur.close()
        self.close_connection()

    def cosineSimilarity(self):
        # Step 1: Vectorize the titles using TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
        tfidf_matrix = vectorizer.fit_transform(self.titles)

        # Step 2: Compute pairwise cosine similarity
        self.matrix = cosine_similarity(tfidf_matrix)
    
    def zeroOut(self):
        threshold = .06
        Perfect = 0
        Good = 0
        Dropped = 0
        max_value = 0
        
        # Iterate over each row and each value in the row
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] < threshold:
                    self.matrix[i][j] = 0
                    Dropped +=1  
                if self.matrix[i][j] >= 1:
                    Perfect +=1
                else:
                    self.matrix[i][j] = round(self.matrix[i][j], 6)
                    if self.matrix[i][j] > max_value:
                        max_value = self.matrix[i][j]
                        maxIndex = [i,j]
                    Good +=1
        print(f"Perfect: {Perfect}")
        print(f"Good: {Good}")
        print(f"Dropped: {Dropped}")
        print(f"Max Value: {max_value}")

    def perform_analysis(self):
        self.get_id_title_data()
        self.cosineSimilarity()
        self.zeroOut()

        self.graph = WeightedGraph()
        self.graph.convert_matrix_to_graph()
        self.relevant_article_index = self.graph.page_ranking_algorithm()
        

    def display_graph(self):
        self.graph.display_graph()
    
    def populate_pageRanker_table(self):
        insert_pageRanker_data = """
            INSERT INTO PAGERANKER_RESULTS (article_id, country, standard_deviation)
            VALUES (%s, %s, %s)
            ON CONFLICT (article_id, country) DO UPDATE 
            SET standard_deviation = EXCLUDED.standard_deviation;
        """
        self.create_connection()
        cur = self.conn.cursor()
        try:
            cur.execute(insert_pageRanker_data, (self.UID[self.relevant_article_index], self.country, 1))
        except Exception as error:
            logging.error("Error while interacting with the database:", error)
        finally:
            if cur:
                cur.close()
        self.close_connection()


    
        

