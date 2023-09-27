import re
import jwt
import os
from ..models.models import User
from ..share.models import Result


def validate_email_and_password(data):
    if not data:
        return Result.failed(data)
    password_regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z])\
                    (?=.*[\.\+\*\?\^\$\,\(\)\[\]\@\!\#\%\^\&\{\}\|\]]).{8,}$"
    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if not re.fullmatch(email_regex, data.get('email')):
        return Result.failed(data.get('email'))
    if not re.fullmatch(password_regex, data.get('password')):
        return Result.failed(data.get('password'))
    return Result.success(data)


def login_services(email, password):
    result = User().login(email, password)
    if not result.is_success():
        return Result.failed({"email": email, "password": password})
    else:
        try:
            user = result.data
            user['token'] = jwt.encode(
                {"user_id": user["_id"]},
                os.getenv("SECRET_KEY"),
                algorithm="HS256"
            )
            return Result.success(user)
        except Exception as e:
            return Result.failed(str(e))
