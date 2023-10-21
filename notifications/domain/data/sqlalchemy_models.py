import datetime
from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass