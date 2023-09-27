import os
import psycopg2
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from .database import database
# from .app import app as main_app

# main_app = app.create_app()

# main_app.config.from_object('config.DevelopmentConfig')
#
# url = main_app.config["SQLALCHEMY_DATABASE_URI"]
# connection = psycopg2.connect(url)
#
# manager = Manager(main_app)
#
# manager.add_command("db", MigrateCommand)
#
# if __name__ == "__main__":
#     manager.run()
#     main_app.run(debug=True)
