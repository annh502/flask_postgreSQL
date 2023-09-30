from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from database.database import db


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    content = mapped_column(db.String(1000), nullable=False)
    created_at = mapped_column(db.DateTime(timezone=True), default=func.now())
    updated_at = mapped_column(
        db.DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    def __init__(self, content):
        self.content = content
<<<<<<< HEAD

    def __repr__(self):
        return str(
            {"id": self.id,
             "content": self.content,
             "created_at": self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
             "updated_at": self.updated_at.strftime("%m/%d/%Y, %H:%M:%S")
             }
        )
=======
>>>>>>> 13ab5df58cd4d788ba35939baf9dcef94ceed2bc
