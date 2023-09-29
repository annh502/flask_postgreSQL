from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from database.database import db


class Like(db.Model):
    __tablename__ = "likes"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    created_at = mapped_column(db.DateTime(timezone=True), default=func.now())