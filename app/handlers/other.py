from aiogram import Router
from aiogram.types import Message

from app.services.parser_service import ParserService

other_router = Router()


@other_router.message()
async def handle_message(message: Message):
    try:
        channel_url = message.text
        videos = await ParserService.parse_channel(channel_url)
        response = ''.join(
            [f'Название:\n {video["title"]}\n'
             f'Описание:\n {video["description"]}\n'
             f'Количество просмотров:\n {video["views"]}\n'
             f'Ссылка:\n {video["link"]}\n\n' for video in videos]
        )
        await message.answer(response)
    except Exception as e:
        await message.answer(f'Произошла ошибка: {str(e)}')
