# a decorator applied to wrapper to make it look like wrapped func
from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from models import models


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return unauthorized("Authentication Token is missing!")

        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = models.User().get_by_id(data["user_id"])
            if current_user is None:
                return unauthorized("Invalid Authentication token!")
            if not current_user["active"]:
                abort(403)

        except Exception as e:
            return internal_server_error("Something went wrong")

        return f(current_user, *args, **kwargs)

    return decorated


