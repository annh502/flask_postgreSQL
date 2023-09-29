from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from database.database import db


class PostLike(db.Model):
    __tablename__ = "likes"
    like_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("likes.id"), primary_key=True)
    post_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("posts.id"), nullable=False, primary_key=True)
    author_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True
    )

    def __init__(self, like_id, post_id, author_id):
        self.like_id = like_id
        self.post_id = post_id
        self.author_id = author_id
