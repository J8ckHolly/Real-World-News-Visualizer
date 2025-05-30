import os
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
import time
import logging

"""
Filename: core_db_component.py

Author: Jack Holly

Date Created: 2025-01-24

Purpose:
    -Serves as the base case to all PostgreSQL component classes
    -Incorporates loading the .env file with passwords
    -Stores all connections in order to connect to the database
    -Stores method to connect and deconnect from the database
    -Includes a timer class to see how long the object takes to complete 
    an action
"""

class DatabaseCoreComponent():
    
    def __init__(self):  # Add the self argument here!
        self.POSTGRESQL_PASSWORD = self.load_db_password()
        
        # Store the connection fields as an instance variable
        self.connection_fields = {
            "host": "localhost",
            "dbname": "postgres",
            "user": "postgres",
            "password": self.POSTGRESQL_PASSWORD,
            "port": 5432
        }

        self.conn = None  # Initialize the connection attribute to None

    def load_db_password(self):
        try:
            #file_path = r'.\webscraping\.env'
            #load_dotenv(dotenv_path=file_path)

            base_path = Path(__file__).resolve().parent.parent
            env_path = base_path / '.env'
            load_dotenv(dotenv_path=env_path)

            POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
            logging.info("Successfully loaded password in DatabaseCC")
            if POSTGRESQL_PASSWORD is None:
                logging.error("POSTGRESQL_PASSWORD environment variable is not found")
                raise ValueError("POSTGRESQL_PASSWORD environment variable is not found")
            return POSTGRESQL_PASSWORD
        except FileNotFoundError:
            logging.error(f"Error: The file at {base_path} was not found.")
            print(f"Error: The file at {base_path} was not found.")
        except ValueError as ve:
            logging.error(f"Error: In Loading password error")
            print(f"Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    def time_method(self, method, *args, **kwargs):
        start_time = time.time()  
        result = method(*args, **kwargs)
        end_time = time.time()
        
        print(f"Execution time for {method.__name__}: {end_time - start_time:.6f} seconds")
        return result
    
    def create_connection(self):
        try:
            if not self.connection_fields:
                print("Connection fields are not set.")
                return None
            
            self.conn = psycopg2.connect(**self.connection_fields)
            logging.info("Connection established!")
        except psycopg2.Error as e:
            print(f"Error: {e}")
            self.conn = None  # Set conn to None if connection fails
    
    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            logging.info("Connection closed.")
        else:
            logging.info("No connection to close.")
    
    def __del__(self):
        # Destructor will call close_connection
        self.close_connection()
    
    
# Example usage (for testing)
if __name__ == "__main__":
    db_component = DatabaseCoreComponent()
    
    db_component.create_connection()  # Establish connection
    
    
