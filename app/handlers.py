from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from .text import hello

router = Router()


@router.message(CommandStart())
async def cmd_start(msg: Message) -> None:
    """Обрабочик стартовой команды."""
    await msg.answer(hello.format(name=msg.from_user.full_name))
