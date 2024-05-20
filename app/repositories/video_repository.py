from sqlalchemy.future import select

from app.db.models.user import User
from app.db.session import async_session
from app.db.models.video import Video


class VideoRepository:
    """Репозиторий отвечающий за действия с базой данных."""

    async def add_video(self, video: Video):
        """Добавляет видео в базу данных."""
        async with async_session() as session:
            session.add(video)
            await session.commit()
            await session.refresh(video)

    async def get_video_by_id(self, video_id: int):
        """Получает id видео."""
        async with async_session() as session:
            result = await session.execute(
                select(Video).filter(Video.id == video_id)
            )
            return result.scalars().first()

    async def get_channels(self, telegram_user_id: int):
        """Получает список каналов для определенного пользователя."""
        async with async_session() as session:
            result = await session.execute(
                select(Video.channel_name)
                .join(User, Video.user_id == User.id)
                .where(User.telegram_user_id == telegram_user_id)
                .distinct()
            )
            return [row[0] for row in result.fetchall()]

    async def get_videos_by_channel_name(
        self,
        telegram_user_id: int,
        channel_name: str
    ):
        """Получает все видео канала для определенного пользователя."""
        async with async_session() as session:
            result = await session.execute(
                select(Video)
                .join(User, Video.user_id == User.id)
                .where(User.telegram_user_id == telegram_user_id)
                .where(Video.channel_name == channel_name)
            )
            return result.scalars().all()
