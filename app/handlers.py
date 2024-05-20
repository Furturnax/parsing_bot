import re

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message
)

from app import text as t
from app.services.database_service import SavingService
from app.services.parser_service import ParserService
from app.repositories.video_repository import VideoRepository
from app.repositories.user_repository import UserRepository

video_repository = VideoRepository()
router = Router()


class Parsing(StatesGroup):
    """Все состояния ожиданий."""

    waiting_for_channel_url = State()
    waiting_for_video_count = State()
    waiting_choise_channel = State()


@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик стартовой команды."""
    await state.set_state(Parsing.waiting_for_channel_url)
    await message.answer(t.HELLO.format(name=message.from_user.full_name))


@router.message(Parsing.waiting_for_channel_url)
async def process_channel_url(message: Message, state: FSMContext):
    """Обработчик состояния ввода ссылки."""
    channel_url = message.text
    channel_link_pattern = r'https:\/\/rutube\.ru\/channel\/\d+\/?$'
    if re.match(channel_link_pattern, channel_url):
        await message.reply(t.CORRECT_URL)
        await state.update_data(channel_url=channel_url)
        await state.set_state(Parsing.waiting_for_video_count)
    else:
        await message.reply(t.INCORRECT_URL)


@router.message(Parsing.waiting_for_video_count)
async def process_video_count(message: Message, state: FSMContext):
    """Обработчик состояния ввода числа количества ссылок на видео."""
    data = await state.get_data()
    try:
        video_count = int(message.text)
        if video_count <= 0:
            await message.reply(t.NUMBER_ERROR)
            return
    except ValueError:
        await message.reply(t.INTAGER_ERROR)
    channel_url = data['channel_url']
    videos = await ParserService.parse_channel(channel_url, video_count)
    user_id = message.from_user.id
    video_repo = VideoRepository()
    user_repo = UserRepository()
    saving_service = SavingService(video_repo, user_repo)
    await saving_service.save_videos(user_id, videos)
    for video in videos:
        await message.answer(
            f'Название: {video["title"]}\n'
            f'Описание: {video["description"]}\n'
            f'Количество просмотров: {video["views"]}\n'
            f'Ссылка: {video["video_url"]}'
        )
    await state.clear()


@router.message(Command('history'))
async def cmd_history(message: Message, state: FSMContext):
    """Обработчик команды для вывода истории парсинга канала."""
    telegram_user_id = message.from_user.id
    await state.update_data(telegram_user_id=telegram_user_id)
    await state.set_state(Parsing.waiting_choise_channel)
    channels = await video_repository.get_channels(telegram_user_id)
    if channels:
        buttons = [
            InlineKeyboardButton(
                text=channel,
                callback_data=f'channel_{channel}'
            ) for channel in channels
        ]
        grouped_buttons = [buttons[i:i + 4] for i in range(0, len(buttons), 4)]
        keyboard = InlineKeyboardMarkup(inline_keyboard=grouped_buttons)
        await message.answer(t.CHOISE_CHANNEL, reply_markup=keyboard)
    else:
        await message.answer(t.EMPTY_HISTORY)


@router.callback_query(F.data.startswith('channel_'))
async def process_channel_choice(callback_query: CallbackQuery):
    """Отлавливает запрос с клавиатуры раздела каналы."""
    channel_name = callback_query.data[len('channel_'):]
    telegram_user_id = callback_query.from_user.id
    videos = await video_repository.get_videos_by_channel_name(
        telegram_user_id,
        channel_name
    )
    if videos:
        buttons = [
            InlineKeyboardButton(
                text=video.title,
                callback_data=f'video_{video.id}'
            ) for video in videos
        ]
        grouped_buttons = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]
        keyboard = InlineKeyboardMarkup(inline_keyboard=grouped_buttons)
        await callback_query.message.answer(
            t.CHOISE_VIDEO,
            reply_markup=keyboard
        )
    else:
        await callback_query.message.answer(
            f'У канала {channel_name} нет видео.'
        )


@router.callback_query(F.data.startswith('video_'))
async def process_video_choice(callback_query: CallbackQuery):
    """Отлавливает запрос с клавиатуры раздела о видео."""
    video_id = int(callback_query.data[len('video_'):])
    video = await video_repository.get_video_by_id(video_id)
    if video:
        await callback_query.message.answer(
            f'Название: {video.title}\n'
            f'Описание: {video.description}\n'
            f'Количество просмотров: {video.views}\n'
            f'Ссылка: {video.video_url}'
        )
    else:
        await callback_query.message.answer(t.VIDEO_NOT_FOUND)


@router.message()
async def handle_message(message: Message):
    """Обработчик любого неопределенного сообщения."""
    await message.answer(t.EMPTY_MESSAGE)
