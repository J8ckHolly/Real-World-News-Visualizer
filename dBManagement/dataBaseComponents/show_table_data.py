from .core_db_component import DatabaseCoreComponent
from psycopg2 import sql
import logging

"""
Filename: show_table_data.py

Author: Jack Holly

Date Created: 2025-01-24

Purpose:
    - Show table data when prompted for a table
    -@Inputs: None
    -@Outputs: Print Statements
    -@Actions: Shows Table Data
"""
class ShowTableData(DatabaseCoreComponent):
    def __init__(self):
        super().__init__()
        self.tableNames = []  # Initialize the list to hold table names
        self.show_table_data()
        self.__del__()

    def show_table_data(self):
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
            for table in tables:
                self.tableNames.append(table[0])
            
            #Print Table Names
            print("\nAvailable Table Names:")
            for table in self.tableNames:
                print("-", table)

            choice = input("Enter table to show data: ").strip()

            if choice not in self.tableNames:
                print(f"'{choice}' is not a valid table name.")
                return

            # Safely insert table name
            query = sql.SQL("SELECT * FROM {} LIMIT 10").format(sql.Identifier(choice))
            cur.execute(query)
            rows = cur.fetchall()

            # Get column names
            colnames = [desc[0] for desc in cur.description]

            print(f"\nShowing up to 10 rows from table: {choice}")
            print(" | ".join(colnames))
            for row in rows:
                print(" | ".join(str(value) for value in row))
            
        except Exception as error:
            logging.info("Error while interacting with the database: %s", error)
        finally:
            if cur:
                cur.close()
            self.close_connection()

    


# Example usage (for testing)
if __name__ == "__main__":
    print("hi")
    tableDel = ShowTableData()
