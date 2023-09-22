import datetime
from database.database import db
from sqlalchemy.orm import Mapped, mapped_column


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String(150), unique=True)
    password: Mapped[str] = mapped_column(db.String(150))
    username: Mapped[str] = mapped_column(db.String(150), unique=True)
    posts = db.relationship("Post", backref="author", lazy="select")
    registered_on = mapped_column(db.DateTime, nullable=False)
    admin: Mapped[bool] = mapped_column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, username, password, admin=False):
        self.email = email
        self.username = username
        self.password = password

    
    
