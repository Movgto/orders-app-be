from __future__ import annotations
from app.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.business import Business
    from app.models.order import Order

class Table(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(nullable=False)
    business_id: Mapped[int] = mapped_column(ForeignKey('business.id', ondelete='CASCADE'), nullable=False)
    business: Mapped['Business']= relationship(
        'Business',
        back_populates='tables'        
    )
    
    orders: Mapped[list['Order']] = relationship(
        'Order',
        back_populates='table',
        cascade='all, delete-orphan',
        lazy='selectin'
    )