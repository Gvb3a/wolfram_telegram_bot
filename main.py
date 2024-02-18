import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from datetime import datetime
from wolfram import main_wolfram
from aiogram.types import InputMediaPhoto
from config import bot_token


bot = Bot(bot_token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(text=f"Hello, {message.from_user.full_name}! Enter what you want to calculate or know about")


@dp.message()
async def wolfram(message: types.Message):
    await message.answer('Loading...')
    resp_list = await asyncio.to_thread(main_wolfram, message.text)
    if resp_list[2]:
        photo1 = InputMediaPhoto(media=resp_list[1])
        photo2 = InputMediaPhoto(media=resp_list[2])

        if resp_list[0] != 'No spoken result available':
            photo1.caption = resp_list[0]

        await message.answer_media_group(media=[photo1, photo2])
    else:
        if resp_list[0] == 'No spoken result available':
            try:
                await message.answer_photo(resp_list[1])
            except:
                await message.answer('Incorrect input')
        else:
            try:
                await message.answer_photo(resp_list[1], caption=resp_list[0])
            except Exception as e:
                print(e)
                await message.answer(resp_list[0])
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
    print(f'A message was sent to user {message.from_user.full_name} at {datetime.now().strftime("%H:%M:%S")}')


async def main():
    await dp.start_polling(bot)

asyncio.run(main())
