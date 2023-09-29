from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from database.database import db


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    content = mapped_column(db.String(1000), nullable=False)
    created_at = mapped_column(db.DateTime(timezone=True), default=func.now())
    updated_at = mapped_column(
        db.DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

