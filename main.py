import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InputMediaPhoto, Message, CallbackQuery, FSInputFile
# from aiogram.client.session.aiohttp import AiohttpSession

from requests import get  # retrieving data from the server (HTTP)
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


@dp.message(CommandStart())  # processing of the start command
async def command_start(message: Message) -> None:  # Sending a welcome message with the user's name
    await message.answer(text=f"Hello, {message.from_user.full_name}! Enter what you want to calculate or know about")
    sql_message('/start', message.from_user.full_name, message.from_user.id, 'Command')
    # calls the sql_message function from the database.py file where the interaction with the database takes place


@dp.message(Command('help'))  # processing of the help command
async def command_help(message: Message) -> None:  # sends a help message and invokes the inline keyboard
    await message.answer(text=help_message, reply_markup=help_keyboard)
    sql_message('/help', message.from_user.full_name, message.from_user.id, 'Command')
    # the code that handles inline keyboard interaction is at the very end


@dp.message(Command('theory'))  # calls the inline keyboard to select a theory
async def theory_command(message: Message) -> None:  # sends an inline keyboard message to select a theory
    await message.answer(text='theory', reply_markup=keyboard)  # keyboard from config.py
    sql_message('/theory', message.from_user.full_name, message.from_user.id, 'Command')


@dp.message(Command('mode'))  # changes the mode from pictures to text or vice versa
async def command_mode(message: Message) -> None:
    if not sql_mode(message.from_user.full_name, message.from_user.id):
        await message.answer(text='Mode changed to pictures')
    else:
        await message.answer(text='Mode changed to text')
    sql_message('/mode', message.from_user.full_name, message.from_user.id, 'Command')
    # sql_mode recognises the current mode. And the mode change happens in sql_message. So we take the opposite value


@dp.message(Command('random_walk'))  # Random walk simulation
async def command_random_walk(message: Message) -> None:  # sends png and pdf with simulation results
    await message.answer('Computing...')  # sends a message that work is in progress
    random_walk_main(str(message.text).lower()[12:], message.message_id)  # calls a function that creates png and pdf
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)  # delete 'Computing...'
    await message.answer_photo(photo=FSInputFile(f'{message.message_id}.png'))  # sends png
    await message.answer_document(document=FSInputFile(f'{message.message_id}.pdf'))  # sends pdf
    remove(f'{message.message_id}.png')  # deletes png
    remove(f'{message.message_id}.pdf')  # deletes pdf
    sql_message(f'/random_walk({str(message.text)[12:].strip()})', message.from_user.full_name, message.from_user.id,
                'Command')


@dp.message()  # Message processing using WolframAlpha API
async def wolfram(message: types.Message) -> None:
    await message.answer('Computing...')  # a temporary message that will be deleted
    mode = sql_mode(message.from_user.full_name, message.from_user.id)  # recognize the mode
    print(f'Request {message.text}({mode}) from {message.from_user.full_name}')  # output the information to the console
    # so that if some error occurs and the request is not entered into the database, we can find out about it.
    query = quote(message.text)  # replace spaces and other special characters with their encoded values
    url = f'https://api.wolframalpha.com/v1/query?appid={show_steps_api}&input=solve+{query}&podstate=Step-by-step%20solution'
    soup = BeautifulSoup(get(url).content, "xml")

    if mode:  # If picture mode
        spok_resp = get(f'https://api.wolframalpha.com/v1/spoken?appid={spoken_api}&i={query}').text
        # Just get the text from the site
        if spok_resp == 'Wolfram Alpha did not understand your input':
            spok_resp = simp_resp = step_resp = False
        else:
            simp_resp = f'https://api.wolframalpha.com/v1/simple?appid={simple_api}&i={query}%3F'  # image link
            try:  # step-by-step solution
                subpod = soup.find("subpod", {"title": "Possible intermediate steps"})
                img_tag = subpod.find("img")
                step_resp = img_tag.get("src") if img_tag else False
            except:
                step_resp = False

        add = f'{spok_resp} {simp_resp} {step_resp}'  # Being a creator, it's a shame not to have access to the answer

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


    else:
        llm_resp = get(f'https://www.wolframalpha.com/api/v1/llm-api?input={query}&appid={show_steps_api}').text
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

        add = (f'https://www.wolframalpha.com/api/v1/llm-api?input={query}&appid={show_steps_api} '
               f'https://api.wolframalpha.com/v1/query?appid={show_steps_api}&input=solve+{query}&podstate=Step-by-step%20solution')

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)

    sql_message(message.text, message.from_user.full_name, message.from_user.id, f'{bool(mode)}: {add}')


@dp.callback_query(F.data == 'help>Mathematics')
async def theory_geometry(callback: CallbackQuery):
    await callback.message.edit_text(text=math_example, reply_markup=inline_help_back, disable_web_page_preview=True)
    await callback.answer()


@dp.callback_query(F.data == 'help>back')
async def theory_geometry(callback: CallbackQuery):
    await callback.message.edit_text(text=help_message, reply_markup=help_keyboard)
    await callback.answer()


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
    sql_launch()


    async def main():
        await dp.start_polling(bot)


    asyncio.run(main())
