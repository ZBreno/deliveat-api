from datetime import time, datetime
from sqlalchemy import ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from typing import List, Optional
from domain.data.enums.week import DayOfWeek
from domain.data.enums.status_order import StatusChoices
from fastapi import UploadFile
from domain.data.enums.role import RoleChoice


class Base(DeclarativeBase):
    pass


class AssociationProductCategory(Base):
    __tablename__ = 'association_product_category'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    product_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('product.id'))
    category_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('category.id'))

    category = relationship(
        "Category", back_populates='products', cascade="all, delete")
    product = relationship(
        "Product", back_populates='categories', cascade="all, delete")


class AssociationProductOrder(Base):
    __tablename__ = 'association_product_order'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    product_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('product.id'))
    order_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('order.id'))

    product = relationship("Product", back_populates="orders")
    order = relationship("Order", back_populates="products")


class AssociationProductBonus(Base):
    __tablename__ = 'association_product_bonus'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    product_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('product.id'))
    product_bonus_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey('product_bonus.id'))

    product = relationship("Product", back_populates="products_bonus")
    product_bonus = relationship("ProductBonus", back_populates="products")


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    cost: Mapped[float]
    image: Mapped[Optional[str]]
    quantity: Mapped[Optional[int]]

    categories = relationship(
        "AssociationProductCategory", back_populates="product", cascade="all, delete", passive_deletes=True)
    orders = relationship("AssociationProductOrder",
                          back_populates="product", cascade="all, delete", passive_deletes=True)
    products_bonus = relationship(
        "AssociationProductBonus", back_populates="product", cascade="all, delete", passive_deletes=True)

    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('user.id'))

    user_products = relationship("User", back_populates="products")

    def __str__(self):
        return self.name


class ProductBonus(Base):
    __tablename__ = 'product_bonus'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    cost: Mapped[float]
    image: Mapped[Optional[str]]
    quantity: Mapped[Optional[int]]

    products = relationship("AssociationProductBonus",
                            back_populates="product_bonus", cascade="all, delete")

    def __str__(self):
        return self.name


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str]
    image: Mapped[Optional[str]]

    products = relationship("AssociationProductCategory",
                            back_populates="category", cascade="all, delete")

    def __str__(self):
        return self.name


class Address(Base):
    __tablename__ = 'address'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    street: Mapped[str]
    city: Mapped[str]
    district: Mapped[str]
    number: Mapped[Optional[str]]
    complement: Mapped[Optional[str]]
    reference_point: Mapped[Optional[str]]

    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('user.id'))

    user_addresses = relationship("User", back_populates="addresses")

    def __str__(self):
        return f"{self.city} - {self.district} / {self.street}"


class Ticket(Base):
    __tablename__ = 'ticket'

    title: Mapped[str]
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    deadline: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    code: Mapped[str]
    description: Mapped[Optional[str]]
    discount: Mapped[float]

    def __str__(self):
        return self.code


class User(Base):
    __tablename__ = 'user'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str]
    delivery_cost: Mapped[Optional[float]]
    time_prepare: Mapped[Optional[str]]
    birthdate: Mapped[Optional[datetime]]
    document: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]
    email: Mapped[str]
    password: Mapped[str]
    instagram: Mapped[Optional[str]]
    profile_picture: Mapped[Optional[str]]
    role: Mapped[RoleChoice] = mapped_column(
        Enum(RoleChoice)
    )

    # is_activate: Mapped[bool]
    isworking = relationship("Operation", back_populates='user_workings')
    addresses = relationship("Address", back_populates='user_addresses')
    products = relationship("Product", back_populates="user_products")

    def __str__(self):
        return self.name


class Operation(Base):
    __tablename__ = 'operations'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    timeout: Mapped[time]
    timein: Mapped[time]
    day: Mapped[DayOfWeek] = mapped_column(
        Enum(DayOfWeek)
    )
    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('user.id'))

    user_workings = relationship("User", back_populates="isworking")

    def __str__(self):
        return self.id


class Rating(Base):
    __tablename__ = 'rating'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    rating: Mapped[int]
    description: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(DateTime)

    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('user.id'))
    order_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('order.id'))

    def __str__(self):
        return f"{self.user_id} - {self.order_id} / {self.rating}"


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    total: Mapped[float]
    observation: Mapped[Optional[str]]
    payment_method: Mapped[str]
    code: Mapped[str]
    status: Mapped[StatusChoices] = mapped_column(
        Enum(StatusChoices)
    )
    created_at: Mapped[datetime] = mapped_column(DateTime)

    address_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('address.id'))
    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('user.id'))
    store_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('user.id'))

    products = relationship("AssociationProductOrder",
                            back_populates="order", cascade="all, delete", passive_deletes=True)

    def __str__(self):
        return f"{self.user_id} / {self.total}"
