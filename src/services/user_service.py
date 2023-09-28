import re
from werkzeug.exceptions import Unauthorized
from src.share.Result import Result
from src.repository import user_repo


def validate_email_and_password(data):
    if not data:
        return Result.failed(data)
    password_regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z])(?=.*[\.\+\*\?\^\$\,\(\)\[\]\@\!\#\%\^\&\{\}\|\]]).{8,}$"
    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if not re.fullmatch(email_regex, data.get('email')):
        return Result.failed(data.get('email'))
    if not re.fullmatch(password_regex, data.get('password')):
        return Result.failed(data.get('password'))
    return Result.success(data)


def validate_email(email):
    try:
        if not email:
            return Result.failed(email)
        email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        if not re.fullmatch(email_regex, email):
            return Result.failed(email)
        return Result.success(email)
    except Exception as e:
        return Result.failed(str(e))


def login_services(email, password):
    result = user_repo.login(email, password)
    if not result.is_success():
        return Result.failed({"email": email, "password": password})
    else:
        try:
            return Result.success(result.data)
        except Exception as e:
            return Result.failed(str(e))


def create_user(name, email, password):
    return user_repo.save(name, email, password)
    # if not result.is_success():
    #     return Result.failed(result.data)
    # else:
    #     return Result.success(result.data)


def update_user(user_id, data):
    return user_repo.update(user_id, data)
    # if not result.is_success():
    #     return Result.failed(result.data)
    # else:
    #     return Result.success(result.data)


def delete_user(user_id):
    return user_repo.delete(user_id)
    # if not result.is_success():
    #     return Result.failed(result.data)
    # else:
    #     return Result.success(result.data)


def disable_account(user_id, account_id):
    admin = user_repo.get_by_id(user_id)
    if not admin.is_success():
        return Result.failed(admin.data)

    account = user_repo.get_by_id(account_id)
    if not account.is_success():
        return Result.failed(account.data)

    admin = admin.data
    if not admin.isAdmin():
        raise Unauthorized("You're not authorized to delete this user!")

    result = user_repo.delete(account_id)
    if not result.is_success():
        return Result.failed(result.data)
    else:
        return Result.success(result.data)
