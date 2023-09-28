# a decorator applied to wrapper to make it look like wrapped func
from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from src.share.api.ResponseEntityFactory import *
from src.models.User import User
from src.repository import user_repo


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return unauthorized("Authentication Token is missing!")

        try:
            data = User.decode_auth_token(token)
            current_user = user_repo.get_by_id(data)
            if current_user is None:
                return unauthorized("Invalid Authentication token!")
            # if not current_user["active"]:
            #     abort(403)
        except jwt.ExpiredSignatureError:
            return unauthorized("Your session is over. Please login again.")
        except jwt.InvalidTokenError:
            return unauthorized("Invalid Auth Token")
        except Exception as e:
            return internal_server_error("Something went wrong: " + str(e))

        return f(current_user, *args, **kwargs)

    return decorated


