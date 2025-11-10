from app.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Table(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(nullable=False)    