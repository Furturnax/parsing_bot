from app.repositories.user_repository import UserRepository
from app.repositories.video_repository import VideoRepository

from app.db.models.video import Video


class SavingService:
    """Сервис по сохранению данных в db."""

    def __init__(self, video_repo: VideoRepository, user_repo: UserRepository):
        self.video_repo = video_repo
        self.user_repo = user_repo

    async def save_videos(
        self,
        telegram_user_id: int,
        videos: list
    ):
        """Сохраняет видео и пользователя в базу данных."""
        user = await self.user_repo.get_or_create_user(telegram_user_id)
        for video_data in videos:
            video = Video(
                title=video_data['title'],
                description=video_data['description'],
                views=video_data['views'],
                video_url=video_data['video_url'],
                channel_name=video_data['channel_name'],
                user_id=user.id
            )
            await self.video_repo.add_video(video)
