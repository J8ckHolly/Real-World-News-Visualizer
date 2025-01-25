from core_db_component import DatabaseCoreComponent
from psycopg2 import sql
import logging

"""
Filename: table_creation.py

Author: Jack Holly

Date Created: 2025-01-24

Purpose:
    -Inherits all attributes of the core_db_component class
    -creates all tables for the system
"""

class TableDeletion(DatabaseCoreComponent):
    def __init__(self):
        super().__init__()
        self.delete_tables()
        self.__del__()
    
    def delete_tables(self):
        try:
            self.create_connection()
            cur = self.conn.cursor()

            # Get a list of all tables in the public schema
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public';
            """)

            tables = cur.fetchall()

            # Drop each table
            for table in tables:
                table_name = table[0]
                drop_query = sql.SQL("DROP TABLE IF EXISTS {} CASCADE;").format(
                    sql.Identifier(table_name)
                )
                cur.execute(drop_query)
                logging.info(f"Dropped table {table_name}")

            # Commit the changes
            self.conn.commit()
            logging.info("All tables Deleted")

        except Exception as error:
            logging.info("Error while interacting with the database:", error)
        finally:
            if cur:
                cur.close()
        self.close_connection()