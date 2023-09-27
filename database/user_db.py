from werkzeug.security import generate_password_hash

from ..database.database import db
from ..share.models import Result
from ..models import models
from . import connection


def get_all():
    """Get all users"""
    cur = connection.cursor()
    query = "SELECT * FROM " + models.User.__tablename__
    cur.execute(query)
    books = cur.fetchall()
    cur.close()
    connection.close()
    return books


def get_by_email(email):
    """Get a user by email"""
    user = db.users.find_one({"email": email, "active":True})
    if not user:
        return Result.failed(email)
    user["_id"] = str(user["_id"])
    return Result.success(user)


def encrypt_password(password):
    """Encrypt password"""
    return generate_password_hash(password)


def get_by_id(user_id):
    """Get a user by id"""
    user = db.users.find_one({"_id": int(user_id), "active":True})
    if not user:
        return Result.failed(user_id)
    user["_id"] = str(user["_id"])
    user.pop("password")
    return Result.success(user)


def save(name="", email="", password=""):
    """Create a new user"""
    user = get_by_email(email)
    if user:
        return Result.failed(user)
    new_user = db.users.insert_one(
        {
            "name": name,
            "email": email,
            "password": encrypt_password(password),
            "active": True
        }
    )
    return Result.success(get_by_id(new_user.inserted_id))
