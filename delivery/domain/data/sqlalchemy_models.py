from datetime import date, time
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from typing import List, Optional
from domain.data.enums.week import DayOfWeek


class Base(DeclarativeBase):
    pass


class AssociationProductCategory(Base):
    __tablename__ = 'association_product_category'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    product_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('product.id'))
    category_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('category.id'))

    category = relationship("Category", back_populates='products')
    product = relationship("Product", back_populates='categories')


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

    categories = relationship(
        "AssociationProductCategory", back_populates="product", cascade="all, delete")
    orders = relationship("AssociationProductOrder",
                          back_populates="product", cascade="all, delete")
    products_bonus = relationship(
        "AssociationProductBonus", back_populates="product", cascade="all, delete")

    def __str__(self):
        return self.name


class ProductBonus(Base):
    __tablename__ = 'product_bonus'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    cost: Mapped[float]

    products = relationship("AssociationProductBonus",
                            back_populates="product_bonus", cascade="all, delete")

    def __str__(self):
        return self.name


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str]

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

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    deadline: Mapped[date]
    code: Mapped[str]
    description: Mapped[Optional[str]]
    type: Mapped[str]

    def __str__(self):
        return self.code


class User(Base):
    __tablename__ = 'user'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str]
    birthdate: Mapped[date]
    document: Mapped[str]
    phone: Mapped[Optional[str]]
    email: Mapped[str]
    password: Mapped[str]
    whatsapp: Mapped[Optional[str]]
    instagram: Mapped[Optional[str]]
    role: Mapped[str]
    isworking = relationship("Operation", back_populates='user_workings')
    addresses = relationship("Address", back_populates='user_addresses')

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


class Rating(Base):
    __tablename__ = 'rating'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    rating: Mapped[int]
    description: Mapped[Optional[str]]

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

    address_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('address.id'))
    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('user.id'))
    store_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('user.id'))

    products = relationship("AssociationProductOrder",
                            back_populates="order", cascade="all, delete")

    def __str__(self):
        return f"{self.user_id} / {self.total}"