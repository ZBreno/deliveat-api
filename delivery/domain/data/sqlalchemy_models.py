from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column, backref
from uuid import UUID
from typing import List, Optional

class Base(DeclarativeBase):
    pass


class AssociationProductCategory(Base):
    __tablename__ = 'association_product_category'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey('product.id'))
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey('category.id'))

    category: Mapped['Category'] = relationship('Category', back_populates='product')
    product: Mapped['Product'] = relationship('Product', back_populates='category')


class AssociationProductOrder(Base):
    __tablename__ = 'association_product_order'
    
    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    product_id: Mapped[UUID] = mapped_column(ForeignKey('product.id'))
    product_bonus_id: Mapped[UUID] = mapped_column(ForeignKey('product.id'))
    order_id: Mapped[UUID] = mapped_column(ForeignKey('order.id'))

    product: Mapped['Product'] = relationship(back_populates="products")
    product_bonus: Mapped['Product'] = relationship(
        back_populates="products_bonus")
    order: Mapped['Order'] = relationship(back_populates="orders")


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    name: Mapped[str]
    description: Mapped[Optional[str]]
    cost: Mapped[int]

    category: Mapped[List["AssociationProductCategory"]] = relationship("Category", back_populates="product",
                              cascade="all, delete", secondary=AssociationProductCategory)

    orders = relationship("Order", back_populates="order",
                          cascade="all, delete", secondary=AssociationProductOrder)


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str]

    product: Mapped[List["AssociationProductCategory"]] = relationship("Product", back_populates="category",
                            cascade="all, delete", secondary=AssociationProductCategory)


class Address(Base):
    __tablename__ = 'address'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    street = Mapped[str]
    city = Mapped[str]
    district = Mapped[str]
    number = Mapped[str]
    complement = Mapped[Optional[str]]
    reference_point = Mapped[Optional[str]]

    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))

    user: Mapped["User"] = relationship(back_populates="addresses",)


class Ticket(Base):
    __tablename__ = 'ticket'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    deadline: Mapped[date]
    code: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]
    type: Mapped[str]


class User(Base):
    __tablename__ = 'user'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    name: Mapped[str]
    birthdate: Mapped[date]
    document: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    whatsapp: Mapped[Optional[str]] = mapped_column(unique=True)
    instagram: Mapped[Optional[str]] = mapped_column(unique=True)
    role: Mapped[str]

    addresses: Mapped[List['Address']] = relationship(back_populates='user')
    orders: Mapped[List['Order']] = relationship(back_populates='user')
    orders_store: Mapped[List['Order']] = relationship(back_populates='store')
    ratings: Mapped[List['Rating']] = relationship(back_populates='store')

class Rating(Base):
    __tablename__ = 'rating'
    
    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)
    rating: Mapped[int]
    description: Mapped[Optional[str]]
    
    store: Mapped['User'] = relationship('User',back_populates='ratings')
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    order_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    total: Mapped[float]
    observation: Mapped[Optional[str]]
    payment_method: Mapped[str]

    address_id: Mapped[UUID] = mapped_column(ForeignKey('address.id'))
    store_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))

    store: Mapped['User'] = relationship('User',back_populates='orders_store')
    user: Mapped['User'] = relationship('User',back_populates='orders')

    products_bonus: Mapped[List['Product']] = relationship(
        'Product', back_populates='products_bonus', cascade="all, delete", secondary=AssociationProductOrder)
    products: Mapped[List['Product']] = relationship('Product', back_populates="product",
                            cascade="all, delete", secondary=AssociationProductOrder)
