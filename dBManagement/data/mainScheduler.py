import json
from pathlib import Path
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from parserComponents.link_parser import RssParser
from datetime import datetime, timedelta
from parserComponents.article_selection import articleSelector

class mainScheduler:
    #Time Constants
    """
    timeConstants = {
    'classA': 15,
    'classB': 30,
    'classC': 45,
    'classD': 60,
    'classE': 75,
    'classF': 90    
    }"""
    timeConstants = {
    'classA': 3,
    'classB': 4,
    'classC': 5,
    'classD': 6,
    'classE': 7,
    'classF': 8    
    }

    countryCounter = {}
    articlePriorityStack = []


    def __init__(self):
        self.readData()
        #self.executeScheduler()

    def readData(self):
        # Get the directory where the country.json file is located
        file_path = Path(__file__).parent / 'classCategory.json'
        # Open and read the JSON file
        with open(file_path, "r") as file:
            self.data = json.load(file)

    def initializeCountryCounter(self):
        countryCounter = {}
        for key in self.data.keys():
            countries = self.data[key]
            
            for country in countries:
                self.countryCounter[country] = 0

    def createObjectListener(self, country):
        RssParser(country, country_Counter=self.countryCounter, dev=True)

    def createArticleSelector(self, country):
        self.articleSelector = articleSelector(country)

    def getArticleSelection(self):
        pass

    def executeScheduler(self):
        self.scheduler = BackgroundScheduler()
        for key in self.data.keys():
            countries = self.data[key]
            num_countries = len(countries)
            period = self.timeConstants[key]  # Total period in minutes

            # Calculate the staggered interval (in minutes)
            staggered_interval = period / num_countries
            #print(f"{key} has {num_countries} countries")
            #print(f"{key} has a staggered interval of {staggered_interval:.4f} minutes.")

            # Schedule a job for each country at staggered intervals
            for i, country in enumerate(countries):
                delay_minutes = staggered_interval * i
                start_time = datetime.now() + timedelta(minutes=delay_minutes)

                self.scheduler.add_job(
                    self.printStatement,
                    trigger='interval',
                    minutes=period,  # Repeat every full period
                    start_date=start_time,
                    args=[country],
                    id=f"{key}_{country}"
                )
                #print(f"Scheduled job for {country} to start at {start_time.strftime('%H:%M:%S')} every {period} minutes.")

        self.scheduler.start()

    def printCountryCounter(self):
        try:
            print(self.countryCounter)
        except NameError:
            print("Country Counter hasn't been initialized yet")

    def printStatement(self, country):
        print(country)

    def printPriorityQuene(self):
        print(self.articlePriorityStack)

            

if __name__ == "__main__":
    print("Running Locally")
    mainScheduler()