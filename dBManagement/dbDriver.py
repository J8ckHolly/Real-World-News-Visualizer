import sys
import logging
import os
from dataBaseComponents.table_deletion import TableDeletion 
from dataBaseComponents.table_creation import TableCreation
from dataBaseComponents.core_db_component import DatabaseCoreComponent
from dataBaseComponents.show_table_data import ShowTableData
from parserComponents.article_selection import articleSelector
from parserComponents.link_parser import RssParser
from data.mainScheduler import mainScheduler

current_working_directory = os.getcwd()
print(current_working_directory)

logging.basicConfig(
    level=logging.DEBUG,
    #format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    format='%(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', mode='w'),  # Log to file 'app.log'
        logging.StreamHandler()          # Optionally also log to console
    ]
)

logging.getLogger('apscheduler').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

def testing_menu():
    db_core = None  # To store the Core DB Component if created

    while True:
        print("\nTesting Options:")
        print("1. Delete All Tables")
        print("2. Create All Tables")
        print("3. Delete Table Data")
        print("4. Create Core DB Component")
        print("5. Show Table Data")
        print("6. Enter Scheduler Menu")
        print("7. Return to Main Menu")

        choice = input("Enter a number (1-7): ").strip()

        if choice == "1":
            print("Deleting all tables...")
            TableDeletion()
        elif choice == "2":
            print("Creating all tables...")
            TableCreation()
        elif choice == "3":
            print("Deleting table data...")
            # Call your function to delete table data here
        elif choice == "4":
            print("Creating a Core DB Component...")
            DatabaseCoreComponent()
        elif choice == "5":
            print("Showing table data...")
            ShowTableData()
        elif choice == "6":
            print("Entering scheduler menu...")
            scheduler_menu()
        elif choice == "7":
            print("Returning to main menu...\n")
            break
        else:
            print("Invalid selection. Please enter a number between 1 and 7.")




def production_menu():
    while True:
        print("\nProduction Options:")
        print("1. Deploy application")
        print("2. Monitor services")
        print("3. Return to main menu")

        choice = input("Enter 1, 2, or 3: ").strip()

        if choice == "1":
            print("Deploying application...")
            # Your production logic here
        elif choice == "2":
            print("Monitoring services...")
            # Your production logic here
        elif choice == "3":
            print("Returning to main menu...\n")
            break
        else:
            print("Invalid selection. Please try again.")

def scheduler_menu():
    scheduler = mainScheduler()
    while True:
        print("\nScheduler Options:")
        print("1. Initialize country counter")
        print("2. Print country counter")
        print("3. Execute scheduler")
        print("4. Create Object Listener")
        print("5. Create Article Selector")
        print("6. Show Priority Pipeline")
        print("7. Get Article Selection")
        print("8. Return to testing menu")

        choice = input("Enter a number (1-8): ").strip()

        if choice == "1":
            print("Initializing country counter...")
            scheduler.initializeCountryCounter()
        elif choice == "2":
            print("Printing country counter...")
            scheduler.printCountryCounter()
        elif choice == "3":
            print("Executing scheduler...")
            scheduler.executeScheduler()
            print("Scheduler is now running in the background.")
        elif choice == "4":
            print("Creating new listener...")
            country = input("Enter the Country for listening to events: ")
            scheduler.createObjectListener(country)
        elif choice == "5":
            print("Creating Article Selector...")
            country = input("Enter the Country for listening to events: ")
            scheduler.createArticleSelector(country)
        elif choice == "6":
            print("Showing Priority Pipeline...")
            scheduler.printPriorityQuene()
        elif choice == "7":
            print("Making Article Selection...")
            #Have to Edit this
            scheduler.articleSelector.perform_analysis()
        elif choice == "8":
            print("Returning to testing menu...\n")
            break
        else:
            print("Invalid selection. Please enter a number between 1 and 8.")




def main():
    while True:
        print("Select environment:")
        print("1. Testing")
        print("2. Production")
        print("3. Exit")

        choice = input("Enter 1, 2, or 3: ").strip()

        if choice == "1":
            testing_menu()
        elif choice == "2":
            production_menu()
        elif choice == "3":
            print("Exiting program. Goodbye!")
            sys.exit()
        else:
            print("Invalid selection. Please enter 1, 2, or 3.\n")

if __name__ == "__main__":
    main()
