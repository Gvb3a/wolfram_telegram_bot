import json
import requests
import asyncio
import aiohttp
import aiofiles
import os
import inspect

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InputMediaPhoto, Message, FSInputFile

from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import detectlanguage
from urllib.parse import quote
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

from database import sql_launch, sql_message
from random_walk import random_walk_main
"""
from .database import sql_launch, sql_message, sql_statistic
from .random_walk import random_walk_main
"""

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')
simple_api = os.getenv('SIMPLE_API')
show_steps_api = os.getenv('SHOW_STEP_API')
simple_tex_api = os.getenv('SIMPLE_TEX_API')
detect_language_api = os.getenv('DETECT_LANGUAGE_API')

bot = Bot(bot_token)
dp = Dispatcher()
detectlanguage.configuration.api_key = detect_language_api
groq_client = Groq(api_key=os.getenv('GROQ_API'))

prompt = """You will need to turn the user's request into a correct one for wolfram alpha (you get the ones that WolframAlpha doesn't understand).

Answer in the following format:

Thought: Think about what the user wanted to write or get Action 
Action Input: What goes into WolframAlpha
"""


def get_dir_path():
    frame = inspect.currentframe()
    caller_frame = frame.f_back
    caller_file_path = caller_frame.f_code.co_filename
    return os.path.dirname(caller_file_path)

json_path = get_dir_path() + '\\text.json'

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

    sql_message(message='/start', name=name, username=username, user_id=user_id, add='')  # database


@dp.message(Command('help'))  # /help
async def command_help(message: Message) -> None:
    language = message.from_user.language_code

    with open(json_path, "r", encoding='utf-8') as file:
        data = json.load(file)
        help_message = data['help'].get(language, data['help']['en'])

    await message.answer(text=help_message, parse_mode='Markdown')
    sql_message('/help', message.from_user.full_name, message.from_user.username, message.from_user.id, add='')


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
                message.from_user.id, add='')


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
        add = f'Recognition({text}, conf={confidence}).'

        if int(confidence * 100) <= 2 or text == '[DOCIMG]':
            message_text = 'Failed to recognise text'
        else:
            message_text = f'Data: `${text}$`\nConfidence: {confidence}%'
    else:
        text = 'Error'
        add = f'Recognition error({response.status_code}'
        message_text = f'Error {response.status_code}. If the image is fine, please contact admin @gvb3a'

    file_obj = file[0][1][1]
    file_obj.close()  # you can't delete a file without it
    os.remove(file_name)

    return message_text, text, add


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


def groq_api(messages: list, model: str = 'llama-3.1-70b-versatile') -> str:
    response = groq_client.chat.completions.create(
            messages=messages,
            model=model)
    return str(response.choices[0].message.content)



async def ask_wolfram_alpha(text: str) -> tuple[str, list]:
    '''Asynchronous function. Returns quick response, step by step solution text and downloaded image paths (simple(page) and step by step)'''
    # all three queries take 2 seconds

    quick_answer = 'Wolfram|Alpha did not understand your input'

    if 'Wolfram|Alpha did not understand your input' in quick_answer:
        print(f'Wolfram|Alpha did not understand {text}. Ask llm')
        messages = [
            {'role': 'user', 'content': prompt},
            {'role': 'user', 'content': text}
        ]
        answer = groq_api(messages=messages)
        action_input_index = answer.index('Action Input:')+len('Action Input:')
        text = answer[action_input_index:].strip().lower()
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


def speech_recognition(file_name: str) -> str:
    with open(file_name, "rb") as file:
        translation = groq_client.audio.transcriptions.create(
        file=(file_name, file.read()),
        model="whisper-large-v3")
            
        text = translation.text

    return str(text).strip()


@dp.message((F.text | F.photo | F.voice))  # Message processing using WolframAlpha API (if photo, SimpleTex api is also used)
async def wolfram(message: types.Message) -> None:
    add = ''
    if message.photo or message.voice:

        await message.answer('Recognition...')

        if message.photo:
            file_name = await download_file_for_id(file_id=message.photo[-1].file_id, extension='png')
            message_text, text, add = recognition(file_name)

        else:
            file_name = await download_file_for_id(file_id=message.voice.file_id, extension='mp3')
            text = speech_recognition(file_name=file_name).strip()
            add = f'Recognition: {text}'
            message_text = f'Recognition: {text}'
            os.remove(file_name)


        await message.answer(text=message_text, parse_mode='Markdown')
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id + 1)
        a = 3  # this is necessary for successful deletion of the processing message at the end



    else:
        text = message.text
        a = 1

    await message.answer('Computing...')  # a temporary message that will be deleted
    
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
    
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + a)

    for image in images:
        os.remove(image)
    add += result
    sql_message(text, message.from_user.full_name, message.from_user.username, message.from_user.id, add)


if __name__ == '__main__':
    sql_launch()
    dp.run_polling(bot, skip_updates=True)