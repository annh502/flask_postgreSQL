from werkzeug.security import check_password_hash
from sqlalchemy.orm import Mapped, mapped_column
from ..share.models import Result
from ..database.database import db
from sqlalchemy.sql import func
from ..database import user_db as user_db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String(150), unique=True)
    password: Mapped[str] = mapped_column(db.String(150))
    username: Mapped[str] = mapped_column(db.String(150), unique=True)
    posts = db.relationship("Post", backref="author", lazy="select")
    registered_on = mapped_column(db.DateTime, nullable=False)
    admin: Mapped[bool] = mapped_column(db.Boolean, nullable=False, default=False)

    def __init__(self):
        pass

    def create_user(self, email, username, password, admin=False):
        self.email = email
        self.username = username
        self.password = password

    @staticmethod
    def login(email, password):
        """Login a user"""
        user = user_db.get_by_email(email)
        if not user:
            return Result.failed(email)
        elif not check_password_hash(user["password"], password):
            return Result.failed(password)
        user.pop("password")
        return Result.success(user)



class Post(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255), nullable=False)
    short_description: Mapped[str] = mapped_column(db.String(300))
    body: Mapped[str] = mapped_column(db.Text, nullable=False)
    date = mapped_column(db.DateTime(timezone=True), default=func.now())

    def __init__(self, title, short_description, body):
        self.title = title
        self.short_description = short_description
        self.body = body

    def __repr__(self):
        return"<id {}".format(self.id)
    
