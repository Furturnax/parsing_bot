from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.text import hello

router = Router()


@router.message(Command('start'))
async def cmd_start(msg: Message) -> None:
    """Обрабочик стартовой команды."""
    await msg.answer(hello.format(name=msg.from_user.full_name))
