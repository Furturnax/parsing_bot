import asyncio
import os
import logging
import sys

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers import router


async def main() -> None:
    """Точка входа."""
    load_dotenv()
    bot = Bot(token=os.getenv('TG_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stop bot.')
