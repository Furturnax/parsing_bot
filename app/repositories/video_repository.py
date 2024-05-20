from sqlalchemy.future import select
from app.db.session import async_session
from app.db.models.video import Video


class VideoRepository:
    async def add_video(self, video: Video):
        async with async_session() as session:
            session.add(video)
            await session.commit()
            await session.refresh(video)

    async def get_videos_by_user(self, user_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(Video).filter_by(user_id=user_id)
            )
            return result.scalars().all()

    async def get_video_by_id(self, video_id: int) -> Video:
        async with async_session() as session:
            result = await session.execute(
                select(Video).filter(Video.id == video_id)
            )
            return result.scalars().first()
