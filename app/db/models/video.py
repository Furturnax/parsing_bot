from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base


class Video(Base):
    """Модель видео."""

    __tablename__ = 'videos'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )
    title: Mapped[str] = mapped_column(
        String,
        index=True
    )
    description: Mapped[str] = mapped_column(String)
    views: Mapped[String] = mapped_column(String)
    video_url: Mapped[str] = mapped_column(String)
    channel_name: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id')
    )
    user: Mapped['User'] = relationship(
        'User',
        back_populates='videos'
    )
