import os
import psycopg2
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)