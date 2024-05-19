import re

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import Message

from app.text import (
    CORRECT_URL,
    EMPTY_MESSAGE,
    HELLO,
    INCORRECT_URL,
    INTAGER_ERROR,
    NUMBER_ERROR
)
from app.services.parser_service import ParserService

router = Router()


class Parsing(StatesGroup):
    """Состояния ожидания."""
    waiting_for_channel_url = State()
    waiting_for_video_count = State()


@router.message(Command('start'))
async def cmd_start(msg: Message, state: FSMContext) -> None:
    """Обработчик стартовой команды."""
    await state.set_state(Parsing.waiting_for_channel_url)
    await msg.answer(HELLO.format(name=msg.from_user.full_name))


@router.message(Parsing.waiting_for_channel_url)
async def process_channel_url(message: Message, state: FSMContext) -> None:
    """Обработчик состояния ввода ссылки."""
    channel_url = message.text
    channel_link_pattern = r'https:\/\/rutube\.ru\/channel\/\d+\/?$'

    if re.match(channel_link_pattern, channel_url):
        await message.reply(CORRECT_URL)
        await state.update_data(channel_url=channel_url)
        await state.set_state(Parsing.waiting_for_video_count)
    else:
        await message.reply(INCORRECT_URL)


@router.message(Parsing.waiting_for_video_count)
async def process_video_count(message: Message, state: FSMContext) -> None:
    """Обработчик состояния ввода числа количества ссылок на видео."""
    data = await state.get_data()

    try:
        video_count = int(message.text)
        if video_count <= 0:
            await message.reply(NUMBER_ERROR)
            return
    except ValueError:
        await message.reply(INTAGER_ERROR)

    channel_url = data['channel_url']
    videos = await ParserService.parse_channel(channel_url, video_count)
    for video in videos:
        await message.answer(
            f'Название: {video["title"]}\n'
            f'Описание: {video["description"]}\n'
            f'Количество просмотров: {video["views"]}\n'
            f'Ссылка: {video["link"]}'
        )
    await state.clear()


@router.message()
async def handle_message(msg: Message) -> None:
    """Обработчик любого неопределенного сообщения."""
    await msg.answer(EMPTY_MESSAGE)
