from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column, Optional, List
from uuid import UUID


class Base(DeclarativeBase):
    pass


class AssociationProductCategory(Base):
    __tablename__ = 'association_product_catergory'

    id: UUID = mapped_column(primary_key=True, unique=True)

    product_id: UUID = mapped_column(
        ForeignKey('product.uuid'), primary_key=True)
    category_id: UUID = mapped_column(
        ForeignKey('category.uuid'), primary_key=True)

    category: Mapped['Category'] = relationship(back_populates="products")
    product: Mapped['Product'] = relationship(back_populates="categories")


class AssociationProductOrder(Base):
    id: UUID = mapped_column(primary_key=True, unique=True)

    products: UUID = mapped_column(ForeignKey('product.uuid'))
    products_bonus: UUID = mapped_column(ForeignKey('product.uuid'))
    orders: UUID = mapped_column(ForeignKey('order.uuid'))

    product: Mapped['Product'] = relationship(back_populates="products")
    product_bonus: Mapped['Product'] = relationship(
        back_populates="products_bonus")
    order: Mapped['Order'] = relationship(back_populates="orders")


class Product(Base):
    __tablename__ = 'product'

    id: UUID = mapped_column(primary_key=True, unique=True)

    name: Mapped[str]
    description: Mapped[Optional[str]]
    cost: Mapped[int]

    categories = relationship("Category", back_populates="products",
                              cascade="all, delete", secondary=AssociationProductCategory)

    orders = relationship("Order", back_populates="order",
                          cascade="all, delete", secondary=AssociationProductOrder)


class Category(Base):
    __tablename__ = 'category'

    id: UUID = mapped_column(primary_key=True, unique=True)
    name: Mapped[str]

    products = relationship("Product", back_populates="categories",
                            cascade="all, delete", secondary=AssociationProductCategory)


class Address(Base):
    __tablename__ = 'address'

    id: UUID = mapped_column(primary_key=True, unique=True)

    street = Mapped[str]
    city = Mapped[str]
    district = Mapped[str]
    number = Mapped[str]
    complement = Mapped[Optional[str]]
    reference_point = Mapped[Optional[str]]

    user_id: UUID = mapped_column(ForeignKey('user.uuid'))

    user: Mapped["User"] = relationship(back_populates="addresses",)


class Ticket(Base):
    __tablename__ = 'ticket'

    id: UUID = mapped_column(primary_key=True, unique=True)

    deadline: Mapped[date]
    code: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]
    type: Mapped[str]


class User(Base):
    __tablename__ = 'user'

    id: UUID = mapped_column(primary_key=True, unique=True)

    name: Mapped[str]
    birthdate: Mapped[date]
    document: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    whatsapp: Mapped[Optional[str]] = mapped_column(unique=True)
    instagram: Mapped[Optional[str]] = mapped_column(unique=True)
    role: Mapped[str]

    addresses = Mapped[List['Address']] = relationship(back_populates='user')
    orders = Mapped[List['Order']] = relationship(back_populates='user')
    orders_store = Mapped[List['Order']] = relationship(back_populates='store')
    ratings: Mapped[List['Rating']] = relationship(back_populates='store')

class Rating(Base):
    __tablename__ = 'rating'

    
    id: UUID
    rating: Mapped[int]
    description: Mapped[Optional[str]]
    
    store: Mapped['User'] = mapped_column(back_populates='ratings')
    
    user_id: UUID = mapped_column(ForeignKey('user.uuid'))
    order_id: UUID = mapped_column(ForeignKey('user.uuid'))


class Order(Base):
    __tablename__ = 'order'

    id: UUID = mapped_column(primary_key=True, unique=True)

    total: Mapped[float]
    observation: Mapped[Optional[str]]
    payment_method: Mapped[str]

    address_id: UUID = mapped_column(ForeignKey('address.uuid'))
    store_id: UUID = mapped_column(ForeignKey('user.uuid'))
    user_id: UUID = mapped_column(ForeignKey('user.uuid'))

    store: Mapped['User'] = mapped_column(back_populates='orders_store')
    user: Mapped['User'] = mapped_column(back_populates='orders')

    products_bonus = relationship(
        'Product', back_populates='products_bonus', cascade="all, delete", secondary=AssociationProductOrder)
    products = relationship('Product', back_populates="product",
                            cascade="all, delete", secondary=AssociationProductOrder)
