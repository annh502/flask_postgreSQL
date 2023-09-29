from database.database import db
from src.share.Result import Result
from src.models.User import User


def get_all():
    """Get all users"""
    users = User.query.all()
    return users


def get_by_id(user_id):
    """Get a user by id"""
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return Result.failed("User doesn't exist: " + str(user_id))
    return Result.success(user)


def get_by_email(email):
    """Get a user by email"""
    user = User.query.filter_by(email=email).first()
    if not user:
        return Result.failed(email)
    return Result.success(user)


def save(new_user):
    """Create a new user"""
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def update(old_user, user):
    """Update a user"""
    try:
        if user["name"]:
            old_user.username = user['name']
        if user["email"]:
            old_user.email = user["email"]
        db.session.commit()
        return Result.success(str(old_user))
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def delete(user):
    try:
        db.session.delete(user)
        db.session.commit()
        return Result.success(str(user))
    except Exception as e:
        return Result.failed("Cannot save" + str(e))
