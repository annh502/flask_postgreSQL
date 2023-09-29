from sqlalchemy.orm import Mapped, mapped_column

from database.database import db


class PostComment(db.Model):
    __tablename__ = "post_comment"
    comment_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("comments.id"), nullable=False, primary_key=True)
    post_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    author_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    def __init__(self, comment_id, post_id, author_id):
        self.comment_id = comment_id
        self.post_id = post_id
        self.author_id = author_id
