from core_db_component import DatabaseCoreComponent
from table_creation import TableCreation
from table_deletion import TableDeletion
from link_parser import RssParser

systemDelete = TableDeletion()
systemInit = TableCreation()
myParser = RssParser("US")
#myParser.print_time()
myParser.insert_entry()
#myParser.delete_table_data()