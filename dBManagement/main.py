import psycopg2
from password import key

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                        password=key, port=5432)

cur = conn.cursor()
# do something
conn.commit()
cur.close()
conn.close()

