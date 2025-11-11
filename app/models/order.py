from __future__ import annotations
from app.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.product import OrderProduct
    from app.models.table import Table

class Order(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    table_id: Mapped[int] = mapped_column(ForeignKey('table.id', ondelete='CASCADE'), nullable=False)
    
    table: Mapped['Table'] = relationship(
        'Table',
        back_populates='orders'
    )
    
    order_products: Mapped[list['OrderProduct']] = relationship(
        'OrderProduct',
        back_populates='order',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
