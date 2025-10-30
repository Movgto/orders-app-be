from __future__ import annotations
from typing import TYPE_CHECKING, Set
from app.security import hash_password, verify_password, needs_rehash

from app.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, ForeignKey, String, Column, Enum as SAEnum
from enum import Enum

class PermissionEnum(str, Enum):
    add_orders = 'add_orders'
    delete_orders = 'delete_orders'
    update_orders = 'update_orders'

employee_permissions = Table(
    'employee_permissions',
    db.metadata,
    Column('employee_id', ForeignKey('employee.id', ondelete='CASCADE'), primary_key=True),
    Column('permission_name', String, ForeignKey('permission.name'), primary_key=True)
)

if TYPE_CHECKING:
    from app.models.user import User

class Employee(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user: Mapped["User"] = relationship('User', back_populates='employees')

    permissions: Mapped[Set["Permission"]] = relationship(
        'Permission',
        secondary=employee_permissions,
        back_populates='employees',
        collection_class=set        
    )

    def __init__(self, first_name: str, last_name: str, password: str, email: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)
    
    def set_password(self, password: str):
        self.password = hash_password(password)

    def check_password(self, password: str):
        ok = verify_password(password, self.password)

        if ok and needs_rehash(self.password):
            self.set_password(password)

        return ok
    
    def add_permissions(self, permissions: list[PermissionEnum]):
        for perm_enum in permissions:
            permission = Permission.query.filter_by(name=perm_enum).first()

            if not permission:
                permission = Permission(name=perm_enum)
                db.session.add(permission)
            
            self.permissions.add(permission)


class Permission(db.Model):
    name: Mapped[str] = mapped_column(
        SAEnum(PermissionEnum, name='permission_enum', native_enum=False),
        nullable=False,
        primary_key=True
    )
    employees: Mapped[Set["Employee"]] = relationship('Employee', secondary=employee_permissions, back_populates='permissions')

    def __init__(self, name: str):
        self.name = name

