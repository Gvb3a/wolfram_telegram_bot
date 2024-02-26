import asyncio
import requests

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InputMediaPhoto, Message, CallbackQuery
from datetime import datetime
from urllib.parse import quote  # is used to replace spaces and other special characters with their encoded values
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

from config import *
from inline import keyboard, keyboard_geometry
from database import sql_create, sql_launch, sql_command
from streamlit_site import streamlit_message_input, streamlit_message_output

bot = Bot(bot_token)
dp = Dispatcher()
init()


@dp.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer(text=f"Hello, {message.from_user.full_name}! Enter what you want to calculate or know about")
    print(message.from_user.id)
    sql_command('/start', message.from_user.full_name, datetime.now().strftime("%H:%M:%S"))



@dp.message(Command('help'))
async def command_help(message: Message) -> None:
    await message.answer('help message(in development)')
    sql_command('/help', message.from_user.full_name, datetime.now().strftime("%H:%M:%S"))


@dp.message(Command('theory'))  # user selection processing at the very end of the file
async def theory_command(message: Message):
    await message.answer(text='theory', reply_markup=keyboard)  # keyboard from config.py
    sql_command('/theory', message.from_user.full_name, datetime.now().strftime("%H:%M:%S"))


mode = True
@dp.message(Command('mode'))
async def command_mode(message: Message) -> None:
    global mode
    mode = not mode

    if mode:
        await message.answer(text='Mode changed to pictures')
    else:
        await message.answer(text='Mode changed to text')

    sql_command(f'/mode({mode})', message.from_user.full_name, datetime.now().strftime("%H:%M:%S"))



def step_by_step_response(query):

    url = f'https://api.wolframalpha.com/v1/query?appid={show_steps_api}&input=solve+{query}&podstate=Step-by-step%20solution'
    soup = BeautifulSoup(requests.get(url).content, "xml")
    subpod = soup.find("subpod", {"title": "Possible intermediate steps"})

    if mode:
        try:
            img_tag = subpod.find("img")
            return img_tag.get("src") if img_tag else False
        except:
            return False
    else:
        try:
            plain_tag = subpod.find('plaintext')
            return plain_tag.get_text('\n', strip=True).replace('Answer: | \n |', '\nAnswer:\n') if plain_tag else False
        except:
            return False


@dp.message()
async def wolfram(message: types.Message) -> None:
    await message.answer('Calculate...')
    streamlit_message_input(message.text, message.from_user.full_name, mode, datetime.now().strftime("%H:%M:%S"))
    query = quote(message.text)

    if mode:
        spok_resp = requests.get(f'https://api.wolframalpha.com/v1/spoken?appid={spoken_api}&i={query}').text

        if spok_resp == 'Wolfram Alpha did not understand your input':
            await message.answer('Wolfram|Alpha did not understand your input')
            spok_resp = simp_resp = step_resp = False
        else:
            simp_resp = f'https://api.wolframalpha.com/v1/simple?appid={simple_api}&i={query}%3F'
            step_resp = step_by_step_response(query)

        print(f'{Fore.GREEN}{message.text}{Style.RESET_ALL}: {spok_resp} {simp_resp} {step_resp}')
        if step_resp:
            photo1 = InputMediaPhoto(media=simp_resp)
            photo2 = InputMediaPhoto(media=step_resp)

            if spok_resp != 'No spoken result available':
                photo1.caption = spok_resp

            await message.answer_media_group(media=[photo1, photo2])
        elif spok_resp:
            try:
                if spok_resp != 'No spoken result available':
                    await message.answer_photo(photo=simp_resp, caption=spok_resp)
                else:
                    await message.answer_photo(photo=simp_resp)
            except:
                await message.answer(text=f'{spok_resp}\nThe image is too large to send, so if you want to see it, '
                    f'go to https://www.wolframalpha.com/input?i={query}', disable_web_page_preview=True)


    else:
        llm_resp = requests.get(f'https://www.wolframalpha.com/api/v1/llm-api?input={query}&appid={show_steps_api}').text
        if 'Wolfram|Alpha could not understand: ' in llm_resp:
            await message.answer(llm_resp)
        else:
            llm_resp = llm_resp[llm_resp.find('Input:'):llm_resp.rfind('Wolfram|Alpha website result for "')]
            step_resp = step_by_step_response(query)
            await message.answer(f'{llm_resp}\nStep by step solution:\n{step_resp}' if step_resp else llm_resp)

        print(f'{Fore.GREEN}{message.text}{Style.RESET_ALL}: '
              f'https://www.wolframalpha.com/api/v1/llm-api?input={query}&appid={show_steps_api} '
              f'https://api.wolframalpha.com/v1/query?appid={show_steps_api}&input=solve+{query}&podstate=Step-by-step%20solution')

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)

    streamlit_message_output(message.text, message.from_user.full_name, datetime.now().strftime("%H:%M:%S"))





@dp.callback_query(F.data == 'theory>geometry')  # triangleArea, back
async def theory_geometry(callback: CallbackQuery):
    await callback.message.edit_text(text='theory>geometry', reply_markup=keyboard_geometry)
    await callback.answer()

@dp.callback_query(F.data == 'theory>geometry>triangleArea')
async def theory_geometry_trianglearea(callback: CallbackQuery):
    await callback.message.answer_photo(photo='https://i.ibb.co/c2SPNFF/triangle-Area.png', caption='Triangle Area')
    await callback.answer()

@dp.callback_query(F.data == 'theory>geometry>back')
async def theory_geometry_back(callback: CallbackQuery):
    await callback.message.edit_text(text='theory', reply_markup=keyboard)
    await callback.answer()



@dp.callback_query(F.data == 'theory>algebra')
async def theory_geometry(callback: CallbackQuery):
    await callback.answer(text='In development', show_alert=True)



@dp.callback_query(F.data == 'theory>python')
async def theory_geometry(callback: CallbackQuery):
    await callback.answer(text='In development', show_alert=True)



@dp.callback_query(F.data == 'theory>close')
async def inline_close(callback: CallbackQuery):
    await callback.message.edit_text(text='close', reply_markup=None)
    await callback.answer()


if __name__ == '__main__':
    sql_create()
    sql_launch(datetime.now().strftime("%H:%M:%S %d.%m.%Y"))

    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())
