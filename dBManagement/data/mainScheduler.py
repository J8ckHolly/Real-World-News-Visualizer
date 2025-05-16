import json
from pathlib import Path
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta

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
    'classF': 90    
    }
    def __init__(self):
        # Get the directory where the country.json file is located
        file_path = Path(__file__).parent / 'classCategory.json'
        # Open and read the JSON file
        with open(file_path, "r") as file:
            self.data = json.load(file)

        for key in self.data.keys():
            print(key)
        self.scheduler = BackgroundScheduler()
        self.executeScheduler()

    def printStatement(self, country):
        print(country)

    from datetime import datetime, timedelta

    def executeScheduler(self):
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

            

if __name__ == "__main__":
    print("Running Locally")
    mainScheduler()