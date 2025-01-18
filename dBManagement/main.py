import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                        password=POSTGRESQL_PASSWORD, port=5432)

cur = conn.cursor()
# do something
conn.commit()
cur.close()
conn.close()

