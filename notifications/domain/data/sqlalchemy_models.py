from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional


class Base(DeclarativeBase):
    pass


class Notification(Base):
    __tablename__ = 'notification'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    text: Mapped[str]
    phone: Mapped[Optional[str]]

    def __str__(self):
        return f"{self.phone} - {self.text}"
