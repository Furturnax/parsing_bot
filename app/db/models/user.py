from typing import List

from sqlalchemy import Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base


class User(Base):
    """Модель юзера."""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )
    telegram_user_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        index=True,
        nullable=False
    )
    videos: Mapped[List['Video']] = relationship(
        'Video',
        back_populates='user'
    )
