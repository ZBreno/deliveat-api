from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from uuid import UUID
from typing import List, Optional


class Base(DeclarativeBase):
    pass
class AssociationProductCategory(Base):
    __tablename__ = 'association_product_category'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey('product.id'), primary_key=True)
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey('category.id'), primary_key=True)

    category: Mapped['Category'] = relationship(
        back_populates='products')
    product: Mapped['Product'] = relationship(
        back_populates='categories')
class AssociationProductOrder(Base):
    __tablename__ = 'association_product_order'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey('product.id'), primary_key=True)
    order_id: Mapped[UUID] = mapped_column(
        ForeignKey('order.id'), primary_key=True)

    product: Mapped['Order'] = relationship(
        back_populates="products",
    )

    order: Mapped['Product'] = relationship(
        back_populates="orders",
    )
class AssociationProductBonus(Base):
    
    __tablename__ = 'association_product_bonus'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey('product.id'), primary_key=True)
    product_bonus_id: Mapped[UUID] = mapped_column(
        ForeignKey('product_bonus.id'), primary_key=True)
    
    product: Mapped['ProductBonus'] = relationship(
        back_populates="products",
    )

    product_bonus: Mapped['Product'] = relationship(
        back_populates="products_bonus",
    )
class Product(Base):
    
    __tablename__ = 'product'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    name: Mapped[str]
    description: Mapped[Optional[str]]
    cost: Mapped[float]
    
    categories: Mapped[Optional[List['AssociationProductCategory']]] = relationship(back_populates="product",
                                                                                    cascade="all, delete")

    orders: Mapped[Optional[List['AssociationProductOrder']]] = relationship(
        back_populates='order',
        cascade="all, delete",
    )
    
    products_bonus: Mapped[Optional[List['AssociationProductBonus']]] = relationship(
        back_populates='product_bonus',
        cascade="all, delete",
    )

    # orders: Mapped[List['AssociationProductOrder']] = relationship(back_populates="order",
    #                                                                       cascade="all, delete")
    def __str__(self):
        return self.name
class ProductBonus(Base):

    __tablename__ = 'product_bonus'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    name: Mapped[str]
    description: Mapped[Optional[str]]
    cost: Mapped[float]

    
    products: Mapped[List['AssociationProductBonus']] = relationship(
        back_populates='product',
        cascade="all, delete",
    )
    def __str__(self):
        return self.name
class Category(Base):
    __tablename__ = 'category'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str]

    products: Mapped[List['AssociationProductCategory']] = relationship(back_populates="category",
                                                                        cascade="all, delete")
    def __str__(self):
        return self.name
class Address(Base):
    __tablename__ = 'address'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    street: Mapped[str]
    city: Mapped[str]
    district: Mapped[str]
    number:  Mapped[Optional[str]]
    complement: Mapped[Optional[str]]
    reference_point:  Mapped[Optional[str]]

    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))

    user: Mapped["User"] = relationship(back_populates="addresses")

    def __str__(self):
        return f"{self.city} - {self.district} / {self.street}"
class Ticket(Base):
    __tablename__ = 'ticket'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    deadline: Mapped[date]
    code: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]
    type: Mapped[str]

    def __str__(self):
        return self.code
class User(Base):
    __tablename__ = 'user'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    name: Mapped[str]
    birthdate: Mapped[date]
    document: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[Optional[str]] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    whatsapp: Mapped[Optional[str]] = mapped_column(unique=True)
    instagram: Mapped[Optional[str]] = mapped_column(unique=True)
    role: Mapped[str]

    addresses: Mapped[List['Address']] = relationship(back_populates='user')

    def __str__(self):
        return self.name
class Rating(Base):
    __tablename__ = 'rating'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)
    rating: Mapped[int]
    description: Mapped[Optional[str]]

    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    order_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))

    def __str__(self):
        return f"{self.user_id} - {self.order_id} / {self.rating}"
class Order(Base):
    __tablename__ = 'order'

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    total: Mapped[float]
    observation: Mapped[Optional[str]]
    payment_method: Mapped[str]

    address_id: Mapped[UUID] = mapped_column(ForeignKey('address.id'))
    store_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))

    products: Mapped[List['AssociationProductOrder']] = relationship(back_populates="product",
                                                                     cascade="all, delete")

    def __str__(self):
        return f"{self.user_id} / {self.total}"