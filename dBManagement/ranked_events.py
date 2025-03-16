from core_db_component import DatabaseCoreComponent
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
import instructor
import os
import logging

class gptDescriptor():

    def __init__(self, uid=None):
        self.uid = uid
        self.OPENAI_KEY = self.load_openAI_password()

    def load_openAI_password(self):
        try:
            file_path = r'.\webscraping\.env'
            load_dotenv(dotenv_path=file_path)
            OPENAI_PASSWORD = os.getenv('OPENAI_API_KEY')
            logging.info("Successfully loaded OpenAI API key")
            if OPENAI_PASSWORD is None:
                logging.error("OPENAI_API_KEY environment variable is not found")
                raise ValueError("OPENAI_API_KEY environment variable is not found")
            return OPENAI_PASSWORD
        except FileNotFoundError:
            logging.error(f"Error: The file at {file_path} was not found.")
            print(f"Error: The file at {file_path} was not found.")
        except ValueError as ve:
            logging.error("Error: Issue loading OpenAI API key")
            print(f"Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def get_relevant_info(self):
        self.title = "Yes, America Is Europe’s Enemy Now"
        with open("dBManagement/FireCrawl.txt", "r", encoding="utf-8") as file:
            self.text = file.read()
        self.country = "United States"

    def check_relevant_info(self):
        if self.title and self.text and self.country:
            print("Good")
            return True

    def get_description_plus_city(self):

        class ExtendedEvent(BaseModel):
            country: str = Field(description="Country Relating to article that is not the country in the prompt")
            description: str = Field(description="Describe the effect of the article on this country in the range of 50-75 words")

        class Coordinates(BaseModel):
            latitude: float = Field(description="Latitude of the city mentioned")
            longitude: float = Field(description="Longitude of the city mentioned")

        class EventSummary(BaseModel):
            description: str = Field(description="Summarary of the article in less than 80 words")
            city: str = Field(description="""Closest city mentioned in the article that is located in the country 
                            given in the prompt. If no valid city is found, return the capital city of the country 
                            given in the prompt""")
            coordinates: Coordinates
            extendedDescription: list[ExtendedEvent] = Field(description="Between and including 1 and 3 countries relating to the country in the prompt not including the country. If no countries are related set the data to none")



        client = OpenAI()

        system_prompt = "You are a news writer giving brief and neutral answers."
        
        query = f"""
        Title: {self.title}
        Article: {self.text}
        Country: {self.country}

        Task:
        1. Summarize the article in less than 80 words.
        2. Extract the closest city mentioned in the article that is located in {self.country}.
           If no valid city is found, return the capital city of {self.country}.
        3. Provide the coordinates (latitude, longitude) of the identified city.
        """

        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            response_format=EventSummary
        )

        return completion.choices[0].message.parsed

# Example Usage
myobject = gptDescriptor(1)
myobject.get_relevant_info()
print(myobject.get_description_plus_city())
