from __future__ import annotations
from typing import TYPE_CHECKING

from app.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.security import verify_password, hash_password, needs_rehash
if TYPE_CHECKING:
    from app.models.employee import Employee

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True,  nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    # One-to-many: a User can have multiple Employee records
    employees: Mapped[list["Employee"]] = relationship(
        'Employee',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='selectin'
    )

    def __init__(self, first_name: str, last_name: str, email:str, password: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)
    
    def set_password(self, password: str):
        self.password = hash_password(password)

    def check_password(self, password: str):
        ok = verify_password(password, self.password)
        # If password verification succeeds, check whether the stored hash
        # should be updated to stronger parameters. Pass the stored hash
        # to needs_rehash (not the plaintext password) so Passlib can
        # identify the hash format and decide if an upgrade is needed.
        if ok and needs_rehash(self.password):
            self.set_password(password)
        
        return ok