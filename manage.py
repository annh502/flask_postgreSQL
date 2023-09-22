import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from database import database

app = create_app()

app.config.from_object('config.DevelopmentConfig')

migrate = Migrate(app, database.db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()