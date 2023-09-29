from flask import Flask
from database import database
from database import database
from src.controllers.post_controller import post_route
from src.controllers.user_controller import auth
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'http://127.0.0.1:3000'  # Our API url (can of course be a local resource

def create_app():
    temp_app = Flask(__name__)

    temp_app.config.from_object('config.DevelopmentConfig')

    database.init_app(temp_app)

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Test application"
        }
    )

    temp_app.register_blueprint(auth, url_prefix="/user")
    temp_app.register_blueprint(post_route, url_prefix="/")
    temp_app.register_blueprint(swaggerui_blueprint)

    with temp_app.app_context():
        from manage import migrate

    from src.models.Post import Post
    from src.models.User import User
    from src.models.Comment import Comment
    from src.models.Like import Like
    from src.models.PostComment import PostComment

    return temp_app


run_app = create_app()

# api_app = Api(app=run_app)

if __name__ == "__main__":
    run_app.run(debug=True, port=3000)