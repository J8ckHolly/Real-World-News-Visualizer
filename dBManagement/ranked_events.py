from core_db_component import DatabaseCoreComponent
from dotenv import load_dotenv
from openai import OpenAI
import os
import logging
"""
Filename: table_creation.py

Author: Jack Holly

Date Created: 2025-01-24

Purpose:
    -Inherits all attributes of the core_db_component class
    -Takes in an article_id, 
    -Selects the most relevant article 
    -Need to work on standard deviation
"""
class articleSelector():
    def __init__(self, uid = None):
        self.uid = uid
        self.OPENAI_KEY = self.load_db_password()

    def load_db_password(self):
        try:
            file_path = r'.\webscraping\.env'
            load_dotenv(dotenv_path=file_path)
            OPENAI_PASSWORD = os.getenv('OPENAI_API_KEY')
            logging.info("Successfully loaded password in DatabaseCC")
            if OPENAI_PASSWORD is None:
                logging.error("POSTGRESQL_PASSWORD environment variable is not found")
                raise ValueError("POSTGRESQL_PASSWORD environment variable is not found")
            return OPENAI_PASSWORD
        except FileNotFoundError:
            logging.error(f"Error: The file at {file_path} was not found.")
            print(f"Error: The file at {file_path} was not found.")
        except ValueError as ve:
            logging.error(f"Error: In Loading password error")
            print(f"Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def get_relevant_info(self):
        self.title = "Yes, America Is Europe’s Enemy Now"
        print(os.listdir())
        with open("dBManagement/FireCrawl.txt", "r", encoding="utf-8") as file:
            self.text = file.read()
        self.country = "United States"

    
    def check_relevant_info(self):
        if self.title and self.text and self.country:
            print("Good")
            
    def get_description_plus_city(self):
        client = OpenAI()
        prompt = f"""
            You are a helpful assistant. Given the following article title and content:

            Title: {self.title}
            Article: {self.text}

            Please do the following:
            1. Summarize the article in less than 100 words (flexible range: 90-110 words).
            2. Extract the closest city mentioned in the article that is located in {self.country}. If no valid city is found, return the capital city of {self.country}.
        """
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
                ]
            )

        # Get the summary and city output
        text_output = completion.choices[0].message.content

        print(text_output)



myobject = articleSelector(1)
myobject.get_relevant_info()
#myobject.check_relevant_info()
myobject.get_description_plus_city()
"""
processor = ArticleProcessor("U.S. pressures Kyiv to replace U.N. resolution condemning Russia", "Ukraine")
article_text = "..."  # The article content

# Step 1: Get summary and city
output = processor.generate_summary_and_city(article_text)
summary, city = output.split('\n')  # Assuming output format gives summary and city in separate lines

# Step 2: Lookup latitude/longitude
latitude, longitude = processor.lookup_coordinates(city)

print(f"Summary: {summary}")
print(f"City: {city}, Latitude: {latitude}, Longitude: {longitude}")


"""