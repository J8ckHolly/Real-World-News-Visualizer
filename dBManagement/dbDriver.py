import sys
import logging
import os
from dataBaseComponents.table_deletion import TableDeletion 
from dataBaseComponents.table_creation import TableCreation
from parserComponents.article_selection import articleSelector
from parserComponents.link_parser import RssParser

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

logger = logging.getLogger(__name__)

def testing_menu():
    while True:
        print("\nTesting Options:")
        print("1. Delete All Tables")
        print("2. Create All Tables")
        print("3. Delete Table Data")
        print("4. Create New Listener")
        print("5. PageRank")
        print("6. Get Similarity")
        print("7. Show Table Data")
        print("8. Return to Main Menu")

        choice = input("Enter a number (1-8): ").strip()

        if choice == "1":
            print("Deleting all tables...")
            # Call your function to delete all tables here
        elif choice == "2":
            print("Creating all tables...")
            # Call your function to create all tables here
        elif choice == "3":
            print("Deleting table data...")
            # Call your function to delete table data here
        elif choice == "4":
            print("Creating new listener...")
            # Call your function to create a new listener here
        elif choice == "5":
            print("Running PageRank...")
            # Call your function to run PageRank here
        elif choice == "6":
            print("Getting similarity...")
            # Call your function to get similarity here
        elif choice == "7":
            print("Showing table data...")
            # Call your function to show table data here
        elif choice == "8":
            print("Returning to main menu...\n")
            break
        else:
            print("Invalid selection. Please enter a number between 1 and 8.")

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
