from database.database import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column


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