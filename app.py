from flask import Flask
from database import database
import psycopg2
from src.controllers.user_controller import auth


def create_app():
    temp_app = Flask(__name__)

    temp_app.config.from_object('config.DevelopmentConfig')

    database.init_app(temp_app)

    temp_app.register_blueprint(auth, url_prefix="/user")

    with temp_app.app_context():
        from manage import migrate

    from src.models.Post import Post
    from src.models.User import User

    return temp_app


run_app = create_app()

if __name__ == "__main__":
    run_app.run()