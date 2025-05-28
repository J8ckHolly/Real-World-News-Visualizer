import feedparser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from parserComponents.PageRankingAlgo import WeightedGraph
from dataBaseComponents.core_db_component import DatabaseCoreComponent
import logging
from datetime import datetime, timedelta
"""
Filename: table_creation.py

Author: Jack Holly

Date Created: 2025-01-24

Purpose:
    -Inherits all attributes of the core_db_component class
    -Pulls all articles from article table and runs the pageranker algorithm
    -Selects the most relevant article
    -Cleans articles if the are expired past 2 days
    -Determines standard deviation
"""
class articleSelector(DatabaseCoreComponent):

    reassignArticleThreshold = 0
    zeroOutThreshold = .06

    
    def __init__(self, country):
        super().__init__()
        self.country = country
        self.titles = []
        self.UID = []
        self.relevant_article_index = None
        print("Article Selector Created")

    def clean(self):
        # SQL query to delete articles older than 2 days
        # First should get the most relevant article, then if it is going to get deleted, set the flag to go to pipeline
        delete_articles_query = """
            DELETE FROM article
            WHERE country = %s AND time < CURRENT_TIMESTAMP - INTERVAL '2 days'
        """
        
        delete_dead_articles_query = """
            DELETE FROM dead_article
            WHERE time < CURRENT_TIMESTAMP - INTERVAL '2 days'
        """

        self.create_connection()
        cur = self.conn.cursor()
        try:
            # Deleting articles and dead_articles older than 2 days
            cur.execute(delete_articles_query, (self.country,))
            cur.execute(delete_dead_articles_query, (self.country,))
            
            # Commit the transaction to apply changes
            self.conn.commit()
        except Exception as error:
            self.conn.rollback()  # Rollback in case of error
            logging.error("Error during deletion:", error)
        finally:
            if cur:
                cur.close()
            self.close_connection()

    def get_article_data(self):
        # Makes sure there is data in the article table
        # Gets the SERIAL UID from the database
        get_article_data = """
            SELECT article_id, title
            FROM article
            WHERE country = %s
        """
        self.create_connection()
        cur = self.conn.cursor()
        success = False
        try:
            cur.execute(get_article_data, (self.country,))
            rows = cur.fetchall()

            if not rows:
                logging.warning(f"No articles found for country: {self.country}")
            else:
                self.UID = [row[0] for row in rows]
                self.titles = [row[1] for row in rows]
                success = True

        except Exception as error:
            logging.error(f"Error while interacting with the database: {error}")
        finally:
            if cur:
                cur.close()
            self.close_connection()
        
        return 0 if success else 1

        
    def cosineSimilarity(self):
        # Step 1: Vectorize the titles using TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
        tfidf_matrix = vectorizer.fit_transform(self.titles)

        # Step 2: Compute pairwise cosine similarity
        self.matrix = cosine_similarity(tfidf_matrix)
    
    def zeroOut(self):
        # Zero's out the data with connections less the desired threshold
        Perfect = 0
        Good = 0
        Dropped = 0
        max_value = 0
        
        # Iterate over each row and each value in the row
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] < self.zeroOutThreshold:
                    self.matrix[i][j] = 0
                    Dropped +=1  
                elif self.matrix[i][j] >= 1:
                    Perfect +=1
                else:
                    self.matrix[i][j] = round(self.matrix[i][j], 6)
                    if self.matrix[i][j] > max_value:
                        max_value = self.matrix[i][j]
                        maxIndex = [i,j]
                    Good +=1
        print("Zero Out Analysis")
        print(f"Perfect: {Perfect}")
        print(f"Good: {Good}")
        print(f"Dropped: {Dropped}")
        print(f"Max Value: {max_value}")

    def perform_analysis(self):
        # First cleans the old data from the article table
        # If there is data then it will find the relation between articles, zeros out the connection, makes the 
        # graph, and then runs the pageranking algorithm
        self.clean()
        exit_code = self.get_article_data()
        
        if exit_code == 0:
            #Creating connections and cleaning up
            self.cosineSimilarity()
            self.zeroOut()
            
            #Making the graph
            self.graph = WeightedGraph()
            self.graph.convert_matrix_to_graph(self.matrix)

            # When you make the graph, the matrix you're passing in doesn't automatically assign the uid of the article
            # Therefore you are getting the index of the most popular article which you reference through the self.UID array
            self.relevant_article_index = self.UID[int(self.graph.page_ranking_algorithm())]

            # Print Ranking Score
            print(f"Score is {self.graph.return_adjusted_score()}")
        else:
            print(f"There is no data in the article rows for {self.country}")
        
    def get_correlation(self, uidA, uidB):
        pass
        # Index first UID
        nodeA = None
        # Index second UID
        nodeB = None
        # Get Correlation method from PageRankerAlgo
        self.graph.determine_correlation(nodeA, nodeB)
        
    
    def return_UID(self):
        if self.relevant_article_index:
            return self.relevant_article_index
        else:
            print("PG not yet run")
            return
    
    def get_top_article(self):
        # Retrieves the most populate article
        # if not there set the flag to automatically add to pipeline
        pass

    def get_similarity(self, node): 
        print(self.reassignArticleThreshold)

    def display_graph(self):
        self.graph.display_graph()

    def get_relevant_article_index(self):
        pass
    
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


    
        

