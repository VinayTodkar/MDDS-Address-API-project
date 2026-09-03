import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is not set in .env")

try:
    connection = psycopg2.connect(database_url)

    cursor = connection.cursor()
    cursor.execute("SELECT version();")

    version = cursor.fetchone()[0]

    print("======================================")
    print("PostgreSQL connection successful!")
    print("======================================")
    print(version)

    cursor.close()
    connection.close()

except Exception as error:
    print("PostgreSQL connection failed!")
    print(error)