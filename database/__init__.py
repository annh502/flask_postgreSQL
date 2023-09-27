from .. import app
import psycopg2

url = app.create_app().config['SQLALCHEMY_DATABASE_URI']
connection = psycopg2.connect(url)
