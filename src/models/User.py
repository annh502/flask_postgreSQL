import datetime
import traceback

import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import Mapped, mapped_column
import os
from src.share.Result import Result
from database.database import db
from sqlalchemy.sql import func
from flask import current_app as run_app


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(db.String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(150), nullable=False)
    username: Mapped[str] = mapped_column(db.String(150), unique=True, nullable=False)
    posts = db.relationship("Post", backref="author", lazy="select")
    registered_on = mapped_column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    admin: Mapped[bool] = mapped_column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, username, password, admin=False):
        self.email = email
        self.username = username
        self.password = password

    def __str__(self):
<<<<<<< HEAD
        return str(
            {
                "id": self.id,
                "email": self.email,
                "username": self.username,
                "registered_on": self.registered_on.strftime("%m/%d/%Y, %H:%M:%S")
            }
        )
=======
        return str({"id": self.id,
                "email": self.email,
                "username": self.username,
                "registered_on": self.registered_on})
>>>>>>> 13ab5df58cd4d788ba35939baf9dcef94ceed2bc

    def is_admin(self):
        return self.admin

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }

            return jwt.encode(
                payload,
                run_app.config['SECRET_KEY'],
                algorithm="HS256"
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, run_app.config['SECRET_KEY'], algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("Your session is over. Please login again.")
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError("Invalid Auth Token")
