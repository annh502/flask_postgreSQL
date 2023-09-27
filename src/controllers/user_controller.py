from flask import Blueprint
from flask import request
from ...services.user_services import *
from share.api.ResponseEntityFactory import *
from database import user_db
#
# auth = Blueprint("Users", __name__)


# @auth.route("/users/login", method=["POST"])
def login():
    try:
        data = request.json
        validate_result = validate_email_and_password(data)
        if not validate_result.is_success():
            return bad_request("Invalid input", data)
        else:
            result = login_services(data.get('email'), data.get('password'))
            if not result.success():
                return bad_request("Authentication failed!", result.data)
            else:
                return ok(result.data)

    except Exception as e:
        return internal_server_error(f"System Error: {str(e)}")


# @auth.route("/")
def test():
    return ok(user_db.get_all())
