import asyncio
import json
import requests
import re

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InputMediaPhoto, Message, CallbackQuery, FSInputFile
from aiogram.client.session.aiohttp import AiohttpSession

from os import remove  # delete a file
from urllib.parse import quote  # string encoding into URL
from bs4 import BeautifulSoup

from config import *
from inline import keyboard, keyboard_geometry, help_message, help_keyboard, math_example, inline_help_back
from database import sql_launch, sql_message, sql_mode
from random_walk import random_walk_main

# the code in the comments is intended for online hosting (pythonanywhere)
# session = AiohttpSession(proxy="http://proxy.server:3128")
bot = Bot(bot_token)  # bot = Bot(bot_token, session=session)
dp = Dispatcher()


@dp.message(CommandStart())  # /start
async def command_start(message: Message) -> None:
    name = f'{message.from_user.full_name}({message.from_user.username})'
    # Sending a welcome message with the user's name
    await message.answer(text=f"Hello, {message.from_user.full_name}! Enter what you want to calculate or know about")
    sql_message('/start', name, message.from_user.id, 'Command')  # database


@dp.message(Command('help'))  # /help
async def command_help(message: Message) -> None:
    # sends a help message with an inline keyboard
    await message.answer(text=help_message, reply_markup=help_keyboard, parse_mode='Markdown')
    name = f'{message.from_user.full_name}({message.from_user.username})'
    sql_message('/help', name, message.from_user.id, 'Command')


"""
@dp.message(Command('theory'))  #/theory
async def theory_command(message: Message) -> None:  # sends an inline keyboard message to select a theory
    await message.answer(text='theory', reply_markup=keyboard)  # keyboard from config.py
    name = f'{message.from_user.full_name}({message.from_user.username})'
    sql_message('/theory', name, message.from_user.id, 'Command')
"""


@dp.message(Command('mode'))  # changes the mode from pictures to text or vice versa
async def command_mode(message: Message) -> None:
    name = f'{message.from_user.full_name}({message.from_user.username})'
    if not sql_mode(name, message.from_user.id):
        await message.answer(text='Mode changed to pictures')
    else:
        await message.answer(text='Mode changed to text')
    sql_message('/mode', name, message.from_user.id, 'Command')
    # sql_mode recognises the current mode. And the mode change happens in sql_message. So we take the opposite value


@dp.message(Command('random_walk'))  # Random walk simulation
async def command_random_walk(message: Message) -> None:  # sends png and pdf with simulation results
    await message.answer('Computing...')  # sends a message that work is in progress
    promt = str(message.text)[12:]
    message_id = message.message_id + 1
    await random_walk_main(str(message.text).lower()[12:], message.message_id)  # calls a function that creates png and pdf
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)  # delete 'Computing...'
    await message.answer_photo(photo=FSInputFile(f'{message.message_id}.png'), caption=promt)  # sends png
    await message.answer_document(document=FSInputFile(f'{message.message_id}.pdf'))  # sends pdf
    remove(f'{message.message_id}.png')  # deletes png
    remove(f'{message.message_id}.pdf')  # deletes pdf
    name = f'{message.from_user.full_name}({message.from_user.username})'
    sql_message(f'/random_walk({promt.strip()})', name, message.from_user.id, 'Command')



@dp.message((F.text | F.photo))  # Message processing using WolframAlpha API
async def wolfram(message: types.Message) -> None:
    name = f'{message.from_user.full_name}({message.from_user.username})'
    mode = sql_mode(name, message.from_user.id)  # recognize the mode
    add = 'Pictures. ' if mode else 'Text. '

    no_error = True
    if message.photo:
        await message.answer('Recognition...')
        file_name = f'{message.message_id}.png'
        await message.bot.download(file=message.photo[-1].file_id, destination=file_name)
        header = {"token": simple_tex_api}
        file = [("file", (file_name, open(file_name, 'rb')))]
        response = requests.post('https://server.simpletex.net/api/latex_ocr', files=file, headers=header)
        if response.status_code == 200:
            data = json.loads(response.text)
            latex = str(data['res']['latex'])
            confidence = int(data['res']['conf'] * 100)
            text = latex
            add += f'Recognition({latex}, conf={confidence}).'
            if int(confidence * 100) == 0:
                await message.answer('Failed to recognise text')
                no_error = False
            else:
                await message.answer(f'Data: `${latex}$`\nConfidence: {confidence}%', parse_mode='Markdown')
        else:
            no_error = False
            text = 'Recognition error'
            add += f'Recognition error({response.status_code}'
            await message.answer(f'Error {response.status_code}. If the image is fine, please contact admin @gvb3a')

        file_obj = file[0][1][1]
        file_obj.close()
        remove(file_name)
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id+1)
        a = 3


    else:
        text = message.text
        a = 1

    await message.answer('Computing...')
    query = quote(text)  # replace spaces and other special characters with their encoded values

      # a temporary message that will be deleted

    # so that if some error occurs and the request is not entered into the database, we can find out about it.
    url = f'https://api.wolframalpha.com/v1/query?appid={show_steps_api}&input=solve+{query}&podstate=Step-by-step%20solution'
    soup = BeautifulSoup(requests.get(url).content, "xml")

    if mode and no_error:  # If picture mode
        spok_resp = requests.get(f'https://api.wolframalpha.com/v1/spoken?appid={spoken_api}&i={query}').text
        # Just get the text from the site
        if spok_resp == 'Wolfram Alpha did not understand your input':
            # If spok_resp gives 'Wolfram Alpha did not understand...', there is no point in processing other responses
            spok_resp = simp_resp = step_resp = False
        else:
            simp_resp = f'https://api.wolframalpha.com/v1/simple?appid={simple_api}&i={query}%3F'  # image link
            try:  # step-by-step solution
                subpod = soup.find("subpod", {"title": "Possible intermediate steps"})
                img_tag = subpod.find("img")
                step_resp = img_tag.get("src") if img_tag else False
            except:
                step_resp = False

        if step_resp:  # If a step-by-step solution is in place
            photo1 = InputMediaPhoto(media=simp_resp)
            photo2 = InputMediaPhoto(media=step_resp)

            if spok_resp != 'No spoken result available':  # adding a description if available
                photo1.caption = spok_resp

            await message.answer_media_group(media=[photo1, photo2])
        elif spok_resp:
            spok_resp = '' if spok_resp == 'No spoken result available' else spok_resp + '\n'
            try:
                await message.answer_photo(photo=simp_resp, caption=spok_resp)

            except:  # There are some files that telegram can't send and gives an error
                await message.answer(text=f'{spok_resp}The image is too large to send, so if you want to see it, '
                                          f'go to https://www.wolframalpha.com/input?i={query}',
                                     disable_web_page_preview=True)
        else:
            await message.answer('Wolfram|Alpha did not understand your input')


    elif no_error and mode:
        llm_resp = requests.get(f'https://www.wolframalpha.com/api/v1/llm-api?input={query}&appid={show_steps_api}').text
        try:
            subpod = soup.find("subpod", {"title": "Possible intermediate steps"})
            plain_tag = subpod.find('plaintext')
            step_resp = (plain_tag.get_text('\n', strip=True).
                         replace('Answer: | \n |', '\nAnswer:\n')) if plain_tag else False
        except:
            step_resp = False

        if 'Wolfram|Alpha could not understand: ' in llm_resp:
            await message.answer(llm_resp)
        else:
            llm_resp = llm_resp[llm_resp.find('Input'):llm_resp.find('Wolfram|Alpha website result for')]
            while len(llm_resp) > 4096:
                await message.answer(llm_resp[:4096])
                llm_resp = llm_resp[4096:]
            await message.answer(f'{llm_resp}\nStep by step solution:\n{step_resp}' if step_resp else llm_resp)

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + a)
    sql_message(message.text, name, message.from_user.id, add)


@dp.callback_query(F.data == 'help>Mathematics')
async def theory_geometry(callback: CallbackQuery):
    await callback.message.edit_text(text=math_example, reply_markup=inline_help_back, disable_web_page_preview=True)
    await callback.answer()


@dp.callback_query(F.data == 'help>back')
async def theory_geometry(callback: CallbackQuery):
    await callback.message.edit_text(text=help_message, reply_markup=help_keyboard)
    await callback.answer()


"""
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
"""

if __name__ == '__main__':
    sql_launch()


    async def main():
        await dp.start_polling(bot)


    asyncio.run(main())
