from core_db_component import DatabaseCoreComponent
from table_creation import TableCreation
from table_deletion import TableDeletion
from link_parser import RssParser
from article_selection import articleSelector
import logging

"""
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Log to file 'app.log'
        logging.StreamHandler()          # Optionally also log to console
    ]
)

logger = logging.getLogger(__name__)
"""

#systemDelete = TableDeletion()
#systemInit = TableCreation()
#myParser = RssParser("US")
#myParser.print_time()
#myParser.insert_entry()
#myParser.delete_table_data()
mySelector = articleSelector("US")
#mySelector.get_id_title_data()
#mySelector.clean()
mySelector.perform_analysis()
