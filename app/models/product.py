from __future__ import annotations
from app.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.order import Order

class OrderProduct(db.Model):    
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    
    quantity: Mapped[int] = mapped_column(nullable=False)
    
    order: Mapped['Order'] = relationship(
        'Order',
        back_populates='order_products',        
    )
    
    product: Mapped['Product'] = relationship(
        'Product',
        back_populates='order_products'
    )
    

class Product(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    
    order_products: Mapped[list['OrderProduct']] = relationship(
        'OrderProduct',
        back_populates='product',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
    