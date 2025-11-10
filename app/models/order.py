from app.db import db
from sqlalchemy.orm import Mapped, mapped_column

class Order(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    
