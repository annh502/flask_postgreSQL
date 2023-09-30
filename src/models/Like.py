from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from database.database import db


class Like(db.Model):
    __tablename__ = "likes"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
<<<<<<< HEAD
    created_at = mapped_column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return str(
            {
                "id": self.id,
                "created_at": self.created_at.strftime("%m/%d/%Y, %H:%M:%S")
            }
        )
=======
    created_at = mapped_column(db.DateTime(timezone=True), default=func.now())
>>>>>>> 13ab5df58cd4d788ba35939baf9dcef94ceed2bc
