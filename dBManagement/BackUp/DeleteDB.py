import psycopg2
from psycopg2 import sql
from dBManagement.BackUp.InitializeDB import load_db_password
import getpass

def drop_all_tables():
    # Define the correct password
    correct_password = "1234"

    # Prompt the user for a password
    #user_password = getpass.getpass(prompt="Please enter the password to continue: ")
    user_password = "1234"

    # Check if the entered password matches the correct one
    if user_password == correct_password:
        print("Password correct. Continuing with the program...")
        # Place your program logic here
    else:
        print("Incorrect password. Exiting...")
        exit()  

    try:
        POSTGRESQL_PASSWORD = load_db_password()
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(host="localhost",
                                dbname="postgres",
                                user="postgres",
                                password=POSTGRESQL_PASSWORD, port=5432)
        cursor = conn.cursor()

        # Get a list of all tables in the public schema
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)

        tables = cursor.fetchall()

        # Drop each table
        for table in tables:
            table_name = table[0]
            drop_query = sql.SQL("DROP TABLE IF EXISTS {} CASCADE;").format(
                sql.Identifier(table_name)
            )
            cursor.execute(drop_query)
            print(f"Dropped table {table_name}")

        # Commit the changes
        conn.commit()

    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Call the function to drop all tables
drop_all_tables()
