from __future__ import annotations
from app.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.table import Table
    from app.models.product import Product

# Import User outside TYPE_CHECKING since we use it at runtime in __init__
from app.models.user import User

class Business(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='businesses')
    
    tables: Mapped[list['Table']] = relationship(
        'Table',
        back_populates='business',
        cascade='all, delete-orphan',
        lazy='selectin'
    )

    products: Mapped[list['Product']] = relationship(
        'Product',
        back_populates='business',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
    
    def __init__(self, name: str, user_id: int):
        user: User|None = User.query.get(user_id)
        
        if not user: raise Exception('User not found')
        
        self.name = name
        self.user_id = user_id