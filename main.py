
import os
import inspect
import PIL.Image
import json
import requests

import asyncio
import aiohttp
import aiofiles

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InputMediaPhoto, Message, FSInputFile

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import quote
from datetime import datetime

from deep_translator import GoogleTranslator
import detectlanguage
import google.generativeai as genai


if __name__ == '__main__' or '.' not in __name__:
    from database import sql_launch, sql_message
    from random_walk import random_walk_main
else:
    from .database import sql_launch, sql_message, sql_statistic
    from .random_walk import random_walk_main


def get_dir_path():
    frame = inspect.currentframe()
    caller_frame = frame.f_back
    caller_file_path = caller_frame.f_code.co_filename
    return os.path.dirname(caller_file_path)

json_path = os.path.join(get_dir_path(), 'text.json')
env_path = os.path.join(get_dir_path(), '.env')

load_dotenv(dotenv_path=env_path)
bot_token = os.getenv('BOT_TOKEN')
simple_api = os.getenv('SIMPLE_API')
show_steps_api = os.getenv('SHOW_STEP_API')
simple_tex_api = os.getenv('SIMPLE_TEX_API')
detect_language_api = os.getenv('DETECT_LANGUAGE_API')
genai_api = os.getenv('GENAI_API_KEY')

bot = Bot(bot_token)
dp = Dispatcher()
detectlanguage.configuration.api_key = detect_language_api
genai.configure(api_key=genai_api)
model = genai.GenerativeModel("gemini-1.5-flash")


@dp.message(CommandStart())  # /start
async def command_start(message: Message) -> None:
    name = message.from_user.full_name
    username = message.from_user.username
    user_id = message.from_user.id
    language = message.from_user.language_code

    with open(json_path, "r", encoding='utf-8') as file:
        data = json.load(file)
        start_message = data['start'].get(language, data['start']['en'])

    await message.answer(text=start_message, parse_mode='Markdown', disable_web_page_preview=True)

    sql_message(message='/start', name=name, username=username, user_id=user_id)  # database


@dp.message(Command('help'))  # /help
async def command_help(message: Message) -> None:
    language = message.from_user.language_code

    with open(json_path, "r", encoding='utf-8') as file:
        data = json.load(file)
        help_message = data['help'].get(language, data['help']['en'])

    await message.answer(text=help_message, parse_mode='Markdown')
    sql_message('/help', message.from_user.full_name, message.from_user.username, message.from_user.id)


@dp.message(Command('random_walk'))  # Random walk simulation
async def command_random_walk(message: Message) -> None:  # sends png and pdf with simulation results
    await message.answer('Computing...')  # sends a message that work is in progress
    promt = str(message.text)[12:]
    message_id = message.message_id + 1
    await random_walk_main(str(message.text).lower()[12:],
                           message.message_id)  # calls a function that creates png and pdf
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)  # delete 'Computing...'
    await message.answer_photo(photo=FSInputFile(f'{message.message_id}.png'), caption=promt)  # sends png
    await message.answer_document(document=FSInputFile(f'{message.message_id}.pdf'))  # sends pdf
    os.remove(f'{message.message_id}.png')  # deletes png
    os.remove(f'{message.message_id}.pdf')  # deletes pdf
    sql_message(f'/random_walk({promt.strip()})', message.from_user.full_name, message.from_user.username,
                message.from_user.id)


def detect_language(text: str) -> str:
    '''The input is text, the output is the language of the text.
    
    It is necessary that if the user wrote in a language other than English, save the language and translate the response'''
    try:
        return detectlanguage.simple_detect(text)
    except:  # If the language cannot be determined, it is most likely an equation (For example 3x-1=11) 
        return 'en'
    

def translate(text: str, target_language: str = 'en', source_language: str = 'auto') -> str:
    '''The function translates text from source_language (recognizes itself if nothing is specified) to target_language (en by default).'''
    translated_text = GoogleTranslator(source=source_language, target=target_language).translate(text)
    return translated_text


def recognition(file_name):
    header = {"token": simple_tex_api}
    file = [("file", (file_name, open(file_name, 'rb')))]
    response = requests.post('https://server.simpletex.net/api/latex_ocr', files=file, headers=header)

    if response.status_code == 200:
        data = json.loads(response.text)
        # example: {'status': True, 'res': {'latex': '(a-b)^3=a^3-b^3-3ab(a-b)', 'conf': 0.95109701156}, 'request_id': 'tr_119214373618527781'}
        text = str(data['res']['latex'])
        confidence = int(data['res']['conf'] * 100)

        if int(confidence * 100) <= 2 or text == '[DOCIMG]':
            message_text = 'Failed to recognise text'
        else:
            message_text = f'Data: `${text}$`\nConfidence: {confidence}%'
    else:
        text = 'Error'
        message_text = f'Error {response.status_code}. If the image is fine, please contact admin @gvb3a'

    file_obj = file[0][1][1]
    file_obj.close()

    return message_text, text


def recognition_with_gemini(image_path: str) -> str:
    image = PIL.Image.open(image_path)
    
    text = 'Your task is to convert a picture into a query for Wolfram Alpha. Nothing extra, your entire response will go to Wolfram Alpha'

    response = model.generate_content([text, image])
    print(response.text)
    return response.text.strip()


async def download_image_async(url: str, filename: str):
    '''Asynchronously download an image from a URL. Returns path to image or False'''
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=60) as response:
            
            if response.status == 200:
                async with aiofiles.open(filename, 'wb') as file:
                    await file.write(await response.read())

                full_path = os.path.abspath(filename)
                return full_path
            
            else:
                return False
            

def wolfram_quick_answer(text: str) -> str:
    '''Return wolfram short answer'''
    query = quote(text)
    return requests.get(f'https://api.wolframalpha.com/v1/spoken?appid={simple_api}&i={query}').text


async def wolfram_simple_answer(text: str) -> str | bool:
    '''Return link to wolfram simple answer (asynchronously)'''
    query = quote(text)
    link = f'https://api.wolframalpha.com/v1/simple?appid={simple_api}&i={query}%3F'

    filename = f"wolfram_simple_answer-{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.png"
    path = await download_image_async(link, filename)

    return str(path)


async def wolfram_step_by_step(text: str) -> tuple[str, list]:
    '''Returns a step by step solution in the form of a string and a list of picture links (asynchronously)'''
    query = quote(text)
    url = f'https://api.wolframalpha.com/v1/query?appid={show_steps_api}&input={query}&podstate=Step-by-step%20solution'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.text()
            soup = BeautifulSoup(content, "xml")

            subpods = soup.find_all("subpod", {"title": "Possible intermediate steps"})
            
            step_images = []
            # step_plain = ''

            for subpod in subpods:
                img_tag = subpod.find("img")
                if img_tag:
                    step_resp_img = img_tag.get("src")
                    step_images.append(step_resp_img)
                '''
                plain_tag = subpod.find('plaintext')
                step_resp = plain_tag.get_text('\n', strip=True)
                step_resp = step_resp.replace('Answer: | \n |', '\nAnswer:\n') if plain_tag else False
                if step_resp:
                    step_plain += step_resp + '\n\n'
                '''
            
            nw = datetime.now().strftime('%Y%m%d_%H%M%S%f')
            downloaded_image_paths = await asyncio.gather(*[download_image_async(url, f'wolfram_step_by_step-{nw}-{i}.png') for i, url in enumerate(step_images)])

            return downloaded_image_paths


def genai_text_api(user_message: str):
    # It would be much better to let the model think, but it's an easy task, so that's fine.
    chat = model.start_chat(history=[
    {
        'role': 'model',
        'parts': 'You will need to turn the user\'s request into a correct one for wolfram alpha (you get the ones that WolframAlpha doesn\'t understand). Nothing extra: your entire answer will go to WolframAlpha.',
    },
])
    response = chat.send_message(user_message)
    print(response.text)
    return response.text.strip()


async def ask_wolfram_alpha(text: str) -> tuple[str, list]:
    '''Asynchronous function. Returns quick response, step by step solution text and downloaded image paths (simple(page) and step by step)'''
    # all three queries take 2 seconds
    
    quick_answer = wolfram_quick_answer(text)
    
    if 'Wolfram Alpha did not understand your input' in quick_answer:
        print(f'Ask llm ({text})')
        text = genai_text_api(text)
        quick_answer = wolfram_quick_answer(text)

    simple_answer_task = asyncio.create_task(wolfram_simple_answer(text))
    step_by_step_task = asyncio.create_task(wolfram_step_by_step(text))

    simple_answer_link = await simple_answer_task
    step_images = await step_by_step_task

    images = [image for image in step_images if image]
    if simple_answer_link:
        images.insert(0, simple_answer_link)
    
    return quick_answer, images


async def download_file_for_id(file_id, extension):

    file = await bot.get_file(file_id)
    file_path = str(file.file_path)
    now = datetime.now()
    file_name = f'{now.strftime("%Y%m%d_%H%M%S")}.{extension}'

    await bot.download_file(file_path, file_name)

    return file_name



@dp.message((F.text | F.photo))  # Message processing using WolframAlpha API (if photo, SimpleTex api is also used)
async def wolfram(message: types.Message) -> None:
    
    await message.answer('Computing...')

    if message.photo or message.voice:
            
        file_name = await download_file_for_id(file_id=message.photo[-1].file_id, extension='png')
        
        text = recognition_with_gemini(file_name)
        
        os.remove(file_name)

    else:
        text = message.text
    
    language = detect_language(text=text)
    
    if language != 'en':
        text = translate(text=text, target_language='en', source_language=language)
        
    result, images = await ask_wolfram_alpha(text)
    
    if language != 'en':
        result = translate(text=result, target_language=language, source_language='en')

    caption = result[:1000]  # telegram has a limitation: you can only post a 1000 character message for a photo. Just in case
    media = [InputMediaPhoto(media=FSInputFile(path=images[0]), 
                                            caption=caption)]
    for image in images[1:]:
        media.append(InputMediaPhoto(media=FSInputFile(path=image)))
    await message.answer_media_group(media=media, parse_mode='Markdown')
    
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)

    for image in images:
        os.remove(image)
        
    sql_message(text + f'Result: {result}', message.from_user.full_name, message.from_user.username, message.from_user.id)


if __name__ == '__main__':
    print('Launch')
    dp.run_polling(bot, skip_updates=True)
