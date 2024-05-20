from sqlalchemy.future import select

from app.db.session import async_session
from app.db.models.user import User


class UserRepository:
    """Репозиторий отвечающий за действия с базой данных."""

    async def get_or_create_user(self, telegram_user_id: int) -> User:
        async with async_session() as session:
            result = await session.execute(
                select(User).filter_by(telegram_user_id=telegram_user_id)
            )
            user = result.scalars().first()
            if user is None:
                user = User(telegram_user_id=telegram_user_id)
                session.add(user)
                await session.commit()
                await session.refresh(user)
            return user
