import json
import requests
import shutil
import hashlib

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InputMediaPhoto, Message, CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from os import remove  # delete a file
from urllib.parse import quote  # string encoding into URL
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import detectlanguage

from config import *
from inline import keyboard, keyboard_geometry, help_message, help_keyboard, math_example, inline_help_back
from database import sql_launch, sql_message, sql_mode, sql_change_mode, sql_statistic
from random_walk import random_walk_main
"""
from .config import *
from .inline import keyboard, keyboard_geometry, help_message, help_keyboard, math_example, inline_help_back
from .database import sql_launch, sql_message, sql_mode, sql_change_mode, sql_statistic
from .random_walk import random_walk_main
"""

bot = Bot(bot_token)
dp = Dispatcher()
detectlanguage.configuration.api_key = detect_language_api


@dp.message(CommandStart())  # /start
async def command_start(message: Message) -> None:
    name = f'{message.from_user.full_name}({message.from_user.username})'
    # Sending a welcome message with the user's name
    await message.answer(text=f"Hello, {message.from_user.full_name}! "
                              f"This telegram bot allows you to use Wolfram Alpha "
                              f"absolutely free with step-by-step solution and photo recognition. "
                              f"There is also a translator and you can write in any language you like. "
                              f"Enter what you want to calculate or know or send a photo.")
    sql_message('/start', name, message.from_user.id, 'Command. ')  # database


@dp.message(Command('help'))  # /help
async def command_help(message: Message) -> None:
    # sends a help message with an inline keyboard
    await message.answer(text=help_message, reply_markup=help_keyboard, parse_mode='Markdown')
    name = f'{message.from_user.full_name}({message.from_user.username})'
    sql_message('/help', name, message.from_user.id, 'Command. ')


"""
@dp.message(Command('theory'))  #/theory
async def theory_command(message: Message) -> None:  # sends an inline keyboard message to select a theory
    await message.answer(text='theory', reply_markup=keyboard)  # keyboard from config.py
    name = f'{message.from_user.full_name}({message.from_user.username})'
    sql_message('/theory', name, message.from_user.id, 'Command. ')
"""


@dp.message(Command('mode'))  # changes the mode from pictures to text or vice versa
async def command_mode(message: Message) -> None:
    name = f'{message.from_user.full_name}({message.from_user.username})'
    id = message.from_user.id
    mode = sql_change_mode(name, id)
    if mode:
        await message.answer(text='Mode changed to pictures')
    else:
        await message.answer(text='Mode changed to text')
    sql_message(f'/mode({mode})', name, id, 'Command. ')


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
    sql_message(f'/random_walk({promt.strip()})', name, message.from_user.id, 'Command. ')



@dp.message(Command('statistic'))
async def command_statistic(message: Message) -> None:
    name = f'{message.from_user.full_name}({message.from_user.username})'
    user_id = message.from_user.id
    message_id = message.message_id
    sql_message('/statistic', name, user_id, 'Command. ')

    if user_id in admin_id:
        admin = True
    else:
        admin = False

    sql_statistic(message_id, admin)

    await message.answer_photo(photo=FSInputFile(f'{message_id}.png'), caption='Update - /statistic')
    remove(f'{message_id}.png')


def translate(text, target):
    try:
        detected_language = detectlanguage.simple_detect(text)
        translated_text = GoogleTranslator(source=detected_language, target=target).translate(text)
        return translated_text, detected_language
    except:
        return text, False


def recognition(file_name):
    no_error = True
    header = {"token": simple_tex_api}
    file = [("file", (file_name, open(file_name, 'rb')))]
    response = requests.post('https://server.simpletex.net/api/latex_ocr', files=file, headers=header)

    if response.status_code == 200:
        data = json.loads(response.text)
        text = str(data['res']['latex'])
        confidence = int(data['res']['conf'] * 100)
        add = f'Recognition({text}, conf={confidence}).'

        if int(confidence * 100) <= 2 or text == '[DOCIMG]':
            message_text = 'Failed to recognise text'
            no_error = False
        else:
            message_text = f'Data: `${text}$`\nConfidence: {confidence}%'
    else:
        no_error = False
        text = 'Error'
        add = f'Recognition error({response.status_code}'
        message_text = f'Error {response.status_code}. If the image is fine, please contact admin @gvb3a'

    file_obj = file[0][1][1]
    file_obj.close()
    remove(file_name)

    return message_text, text, add, no_error


def download_image(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)
        return True
    else:
        return False


def step_by_step_response(query, mode, file_name):
    try:  # step-by-step solution
        url = f'https://api.wolframalpha.com/v1/query?appid={show_steps_api}&input=solve+{query}&podstate=Step-by-step%20solution'
        soup = BeautifulSoup(requests.get(url).content, "xml")
        subpod = soup.find("subpod", {"title": "Possible intermediate steps"})

        if mode:
            img_tag = subpod.find("img")
            step_resp = img_tag.get("src") if img_tag else False
            step_resp = download_image(step_resp, file_name)
        else:
            plain_tag = subpod.find('plaintext')
            step_resp = (plain_tag.get_text('\n', strip=True).
                         replace('Answer: | \n |', '\nAnswer:\n')) if plain_tag else False

        return step_resp
    except:
        return False

@dp.message((F.text | F.photo))  # Message processing using WolframAlpha API (if photo, SimpleTex api is also used)
async def wolfram(message: types.Message) -> None:
    name = f'{message.from_user.full_name}({message.from_user.username})'
    mode = sql_mode(name, message.from_user.id)  # recognize the mode
    add = 'Pictures. ' if mode else 'Text. '

    no_error = True
    if message.photo:

        await message.answer('Recognition...')
        file_name = f'{message.message_id}.png'
        await message.bot.download(file=message.photo[-1].file_id, destination=file_name)  # download image

        message_text, text, add_add, no_error = recognition(file_name)
        add += add_add

        await message.answer(text=message_text, parse_mode='Markdown')
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id+1)
        a = 3  # this is necessary for successful deletion of the processing message at the end


    else:
        text = message.text
        a = 1

    await message.answer('Computing...')  # a temporary message that will be deleted

    translated_text, l = translate(text, 'en')
    query = quote(translated_text) # 'quote' replace spaces and other special characters with their encoded values

    if mode and no_error:  # If picture mode
        spok_resp = requests.get(f'https://api.wolframalpha.com/v1/spoken?appid={spoken_api}&i={query}').text
        simp_resp = f'https://api.wolframalpha.com/v1/simple?appid={simple_api}&i={query}%3F'
        simp_file_name = str(message.message_id) + 'simp.png'
        step_file_name = str(message.message_id) + 'step.png'

        wf_understand = True
        if spok_resp == 'Wolfram Alpha did not understand your input':
            # If spok_resp gives 'Wolfram Alpha did not understand...', there is no point in processing other responses
            spok_resp = simp_resp = step_resp = False
            wf_understand = False
            add += 'Did not understand. '

        else:
            simp_resp = download_image(simp_resp, simp_file_name)
            step_resp = step_by_step_response(query, mode, step_file_name)

        if spok_resp == 'No spoken result available':
            spok_resp = ''
        else:
            spok_resp = translate(spok_resp, l)[0]

        try:
            if step_resp:  # If a step-by-step solution is in place
                photo_list = [InputMediaPhoto(media=FSInputFile(simp_file_name), caption=spok_resp), InputMediaPhoto(media=FSInputFile(step_file_name))]
                await bot.send_media_group(chat_id=message.chat.id, media=photo_list, request_timeout=10)
                remove(simp_file_name)
                remove(step_file_name)

            elif wf_understand and simp_resp:
                await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(simp_file_name), caption=spok_resp, request_timeout=10)
                remove(simp_file_name)

            else:
                await message.answer('Wolfram|Alpha did not understand your input')

        except:
            await message.answer(text=f'{spok_resp}\n'
                                      f'Some kind of error. Maybe the image is too big or the admin messed something up')


    elif no_error:
        llm_resp = requests.get(f'https://www.wolframalpha.com/api/v1/llm-api?input={query}&appid={show_steps_api}').text
        step_resp = step_by_step_response(query, mode, False)

        if 'Wolfram|Alpha could not understand: ' in llm_resp:
            await message.answer(llm_resp)

        else:
            llm_resp = llm_resp[llm_resp.find('Input'):llm_resp.find('Wolfram|Alpha website result for')]

            # in telegram there is a limitation on the length of the message, so we send it in parts.
            while len(llm_resp) > 4096:
                await message.answer(llm_resp[:4096])
                llm_resp = llm_resp[4096:]

            await message.answer(f'{llm_resp}\nStep by step solution:\n{step_resp}' if step_resp else llm_resp)

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + a)
    sql_message(text, name, message.from_user.id, add)


@dp.callback_query(F.data == 'help>Mathematics')
async def theory_geometry(callback: CallbackQuery):
    await callback.message.edit_text(text=math_example, reply_markup=inline_help_back, disable_web_page_preview=True)
    await callback.answer()


@dp.callback_query(F.data == 'help>back')
async def theory_geometry(callback: CallbackQuery):
    await callback.message.edit_text(text=help_message, reply_markup=help_keyboard)
    await callback.answer()


def short_answers(query):
    try:
        l = detectlanguage.simple_detect(query)
        query = GoogleTranslator(source=l, target="en").translate(query)
        text = requests.get(f'http://api.wolframalpha.com/v1/result?appid={short_answers_api}&i={quote(query)}').text
        return GoogleTranslator(source='en', target=l).translate(text)
    except:
        return requests.get(f'http://api.wolframalpha.com/v1/result?appid={short_answers_api}&i={quote(query)}').text



@dp.inline_query()
async def inline_q(inline_query: types.InlineQuery):
    query = inline_query.query or 'None'
    l = inline_query.from_user.language_code
    result_id = hashlib.md5(query.encode()).hexdigest()
    if query == 'None':
        answer = 'Enter what you want to calculate or know'
    else:
        answer = short_answers(query)
    item = InlineQueryResultArticle(
        id=result_id,
        input_message_content=InputTextMessageContent(message_text=answer),
        title=answer
    )
    await inline_query.answer([item], cache_time=20)
    name = inline_query.from_user.full_name
    username = inline_query.from_user.username
    uid = inline_query.from_user.id
    sql_message(f'inline query: {query}', f'{name}({username})', uid, f'inline query. {answer}')


# you need to get in there and work on it. It's in too raw a state to leave it.
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
    dp.run_polling(bot, skip_updates=True)
