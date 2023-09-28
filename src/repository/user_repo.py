from werkzeug.security import generate_password_hash, check_password_hash

from database.database import db
from src.share.Result import Result
from src.models.User import User
from . import connection
cur = connection.cursor()


def encrypt_password(password):
    """Encrypt password"""
    return generate_password_hash(password)


def get_all():
    """Get all users"""
    query = "SELECT * FROM " + User.__tablename__
    cur.execute(query)
    users = User.query.all()
    # users = cur.fetchall()
    return users


def get_by_id(user_id):
    """Get a user by id"""
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return Result.failed(user_id)
    return Result.success(user)


def get_by_email(email):
    """Get a user by email"""
    user = User.query.filter_by(email=email).first()
    if not user:
        return Result.failed(email)
    return Result.success(user)


def login(email, password):
    """Login a user"""
    user_result = get_by_email(email)
    user = user_result.data
    if not user_result.is_success():
        return Result.failed(email)
    elif not check_password_hash(user.password, password):
        return Result.failed(password)
    auth_token = user.encode_auth_token(user.id)
    return Result.success(auth_token)


def save(name="", email="", password=""):
    """Create a new user"""
    try:
        user = get_by_email(email)
        if user.is_success():
            return Result.failed("Email exists: " + str(email))
        try:
            new_user = User(email, name, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            auth_token = new_user.encode_auth_token(new_user.id)
            return Result.success(str(auth_token))
        except Exception as e:
            return Result.failed("Cannot save" + str(e))
    except Exception as e2:
        return Result.failed(str(e2))


def update(user_id, data):
    """Update a user"""
    try:
        user_result = get_by_id(user_id)
        if not user_result.is_success():
            return Result.failed(user_id)
        try:
            user = user_result.data
            if data["name"]:
                user.username = data['name']
            if data["email"]:
                user.email = data["email"]
            db.session.commit()
            return Result.success(user_id)
        except Exception as e:
            return Result.failed("Cannot save" + str(e))
    except Exception as e2:
        return Result.failed(str(e2))


def delete(user_id):
    try:
        user_result = get_by_id(user_id)
        if not user_result.is_success():
            return Result.failed(user_id)
        try:
            user = user_result.data
            db.session.delete(user)
            db.session.commit()
            return Result.success(user_id)
        except Exception as e:
            return Result.failed("Cannot save" + str(e))

    except Exception as e2:
        return Result.failed(str(e2))
