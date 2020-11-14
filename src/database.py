import os

import psycopg2


connection = psycopg2.connect(
    database="check_it_api",
    user="check_it_app",
    password=os.getenv("DB_PASSWORD"),
    host="localhost"
)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name VARCHAR);")
connection.commit()