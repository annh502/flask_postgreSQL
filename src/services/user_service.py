import re
from werkzeug.exceptions import Unauthorized

from src.models.User import User
from src.share.Result import Result
from src.repository import user_repo
from werkzeug.security import generate_password_hash, check_password_hash


def encrypt_password(password):
    """Encrypt password"""
    return generate_password_hash(password)


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


def login(email, password):
    """Login a user"""
    try:
        if not validate_email(email):
            return Result.failed(email)
        user_result = user_repo.get_by_email(email)
        user = user_result.data
        if not user_result.is_success():
            return Result.failed(email)
        elif not check_password_hash(user.password, password):
            return Result.failed(password)
        auth_token = user.encode_auth_token(user.id)
        return Result.success(auth_token)
    except Exception as e:
        return Result.failed(str(e))


def create_user(name, email, password):
    try:
        user = user_repo.get_by_email(email)
        if user.is_success():
            return Result.failed("Email exists: " + str(email))
        if name is None:
            return Result.failed("Username must not be null.")
        new_user = User(email, name, generate_password_hash(password))
        return Result.success(new_user.encode_auth_token(new_user.id)) \
            if user_repo.save(new_user).is_success() \
            else Result.failed("Cannot save: ")
    except Exception as e:
        return Result.failed("Error in user services: " + str(e))


def log_out(token):
    try:
        return user_repo.logout(token)
    except Exception as e:
        return Result.failed("Error in user services: " + str(e))


def update_user(user_id, data):
    try:
        user_result = user_repo.get_by_id(user_id)
        if not user_result.is_success():
            return Result.failed(user_id)
        return user_repo.update(user_result.data, data)
    except Exception as e:
        return Result.failed("Error in user services: " + str(e))


def delete_user(user_id):
    try:
        user_result = user_repo.get_by_id(user_id)
        if not user_result.is_success():
            return Result.failed(user_id)
        return user_repo.delete(user_result.data)
    except Exception as e:
        return Result.failed("Error in user services: " + str(e))


def disable_account(user_id, account_id):
    try:
        admin = user_repo.get_by_id(user_id)
        if not admin.is_success():
            return Result.failed(admin.data)

        account = user_repo.get_by_id(account_id)
        if not account.is_success():
            return Result.failed(account.data)

        admin = admin.data
        if not admin.is_admin():
            raise Unauthorized("You're not authorized to delete this user!")

        return user_repo.delete(account.data)
    except Exception as e:
        return Result.failed("Error in user services: " + str(e))
