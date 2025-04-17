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



#systemDelete = TableDeletion()
#systemInit = TableCreation()
#myParser = RssParser("United States")
#myParser.insert_links()
#myParser.delete_table_data()
mySelector = articleSelector("United States")
#mySelector.get_id_title_data()
#mySelector.clean()
mySelector.perform_analysis()
mySelector.populate_pageRanker_table()
