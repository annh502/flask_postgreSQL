from flask import Flask
from database import database

app = Flask(__name__)
if __name__ == '__app__':
    app.run(host='0.0.0.0', port=8000)