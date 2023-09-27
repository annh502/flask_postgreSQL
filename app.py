from flask import Flask
from .database import database
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from .routes.user_routes import user_route
import psycopg2


def create_app():
    main = Flask(__name__)

    main.config.from_object('config.DevelopmentConfig')

    migrate = Migrate(main, database.db)

    database.init_app(main)

    main.register_blueprint(user_route, url_prefix='/')

    # app.register_blueprint(controllers.auth, url_prefix="/")

    from domain.blog.models import Post
    from models.models import User

    return main


main_app = create_app()
manager = Manager(main_app)
manager.add_command("db", MigrateCommand)
url = main_app.config['SQLALCHEMY_DATABASE_URI']
connection = psycopg2.connect(url)


# def create_connection():
#     url = app.config['SQLALCHEMY_DATABASE_URI']
#     return psycopg2.connect(url)

if __name__ == "__main__":
    manager.run()
    app.run(debug=True)
