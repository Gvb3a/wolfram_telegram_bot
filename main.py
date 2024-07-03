import json
import requests
import shutil
import os
# requests, aiogram, bs4, deep_translator, detectlanguage, matplotlib, colorama, g4f, lxml, python-dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InputMediaPhoto, Message, CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from g4f.client import Client
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import detectlanguage
from random import choice

from inline import keyboard, keyboard_geometry, help_message, help_keyboard, math_example, inline_help_back
from database import sql_launch, sql_message, sql_statistic
from random_walk import random_walk_main
"""
from .inline import keyboard, keyboard_geometry, help_message, help_keyboard, math_example, inline_help_back
from .database import sql_launch, sql_message, sql_statistic
from .random_walk import random_walk_main
"""

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
simple_api = os.getenv('SIMPLE_API')  # One api is appropriate for both spoken api and simple api
show_steps_api = os.getenv('SHOW_STEP_API')
simple_tex_api = os.getenv('SIMPLE_TEX_API')
detect_language_api = os.getenv('DETECT_LANGUAGE_API')  # The library I use for translation takes a very long time to process queries like 12x-1=3.
admin_id = int(os.getenv('ADMIN_ID'))


bot = Bot(bot_token)
dp = Dispatcher()
detectlanguage.configuration.api_key = detect_language_api


@dp.message(CommandStart())  # /start
async def command_start(message: Message) -> None:
    name = message.from_user.full_name
    username = message.from_user.username
    user_id = message.from_user.id
    # Sending a welcome message with the user's name
    await message.answer(text=f"Hello, {message.from_user.full_name}! "
                              f"This telegram bot allows you to use Wolfram Alpha "
                              f"absolutely free with step-by-step solution and photo recognition. "
                              f"There is also a translator and you can write in any language you like. "
                              f"Enter what you want to calculate or know or send a photo.")
    sql_message(message='/start', name=name, username=username, user_id=user_id, add='')  # database


@dp.message(Command('help'))  # /help
async def command_help(message: Message) -> None:
    # sends a help message with an inline keyboard
    await message.answer(text=help_message, reply_markup=help_keyboard, parse_mode='Markdown')
    sql_message('/help', message.from_user.full_name, message.from_user.username, message.from_user.id, add='')




@dp.message(Command('random_walk'))  # Random walk simulation
async def command_random_walk(message: Message) -> None:  # sends png and pdf with simulation results
    await message.answer('Computing...')  # sends a message that work is in progress
    promt = str(message.text)[12:]
    message_id = message.message_id + 1
    await random_walk_main(str(message.text).lower()[12:], message.message_id)  # calls a function that creates png and pdf
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)  # delete 'Computing...'
    await message.answer_photo(photo=FSInputFile(f'{message.message_id}.png'), caption=promt)  # sends png
    await message.answer_document(document=FSInputFile(f'{message.message_id}.pdf'))  # sends pdf
    os.remove(f'{message.message_id}.png')  # deletes png
    os.remove(f'{message.message_id}.pdf')  # deletes pdf
    sql_message(f'/random_walk({promt.strip()})', message.from_user.full_name, message.from_user.username, message.from_user.id, add='')



@dp.message(Command('statistic'))
async def command_statistic(message: Message) -> None:
    user_id = message.from_user.id
    message_id = message.message_id
    sql_message('/statistic',  message.from_user.full_name, message.from_user.username, message.from_user.id, add='')

    
    admin = True if user_id == admin_id else False

    sql_statistic(message_id, admin)

    await message.answer_photo(photo=FSInputFile(f'{message_id}.png'), caption='Update - /statistic')
    os.remove(f'{message_id}.png')




def translate(text, target):
    # Usage. First we translate the user's request into English, since wolfram only understands this language
    # We also take the language in which the user sent the request and translate the response into that language.
    try: # in 3x-1=11 we will fail to recognize the language and get an error.
        language = detectlanguage.simple_detect(text)
        translated_text = GoogleTranslator(source=language, target=target).translate(text)
        return translated_text, language
    except:
        return text, 'en'


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


def download_image(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)
        return True
    else:
        return False

def step_by_step_response(query, file_name_prefix):
    try:
        url = f'https://api.wolframalpha.com/v1/query?appid={show_steps_api}&input={query}&podstate=Step-by-step%20solution'
        soup = BeautifulSoup(requests.get(url).content, "lxml")
        
        # Find all subpods with step-by-step solutions
        subpods = soup.find_all("subpod", {"title": "Possible intermediate steps"})
        
        downloaded_files = []
        
        for index, subpod in enumerate(subpods):
            img_tag = subpod.find("img")
            if img_tag:
                step_resp = img_tag.get("src")
                file_name = f"{file_name_prefix}_{index + 1}.png"
                
                if download_image(step_resp, file_name):
                    downloaded_files.append(file_name)
        return downloaded_files if downloaded_files else False
    except Exception as e:
        print('Step by step: ', e)
        return False

def g4f_convert(text):
    try:
        client = Client()
        response = client.chat.completions.create(
            model=choice(['gpt-4', 'gpt-3.5-turbo', 'gpt-4-turbo']),
            messages=[
                {"role": "user", "content": f"""You task is to TRANSFORM the user's query so that it is 
                 UNDERSTANDABLE by Wolfram Alpha. The converted query MUST BE in `. 
                 If it is not possible to convert the query, you answer the query. Query: {text}"""}
            ]
        )
        resp = response.choices[0].message.content
        return resp
    except Exception as e:
        print(f'g4f: {e}')
        return text

def spok_resp_get(text):
        spok_resp = requests.get(f'https://api.wolframalpha.com/v1/spoken?appid={simple_api}&i={requests.utils.requote_uri(text)}').text
        w_not_understand = spok_resp.startswith('Wolfram Alpha did not understand')
        return spok_resp, w_not_understand


@dp.message((F.text | F.photo))  # Message processing using WolframAlpha API (if photo, SimpleTex api is also used)
async def wolfram(message: types.Message) -> None:
    add = ''
    if message.photo:

        await message.answer('Recognition...')
        file_name = f'{message.message_id}.png'
        await message.bot.download(file=message.photo[-1].file_id, destination=file_name)  # download image

        message_text, text, rec_add = recognition(file_name)
        add += rec_add
        await message.answer(text=message_text, parse_mode='Markdown')
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id+1)
        a = 3  # this is necessary for successful deletion of the processing message at the end


    else:
        text = message.text
        a = 1

    await message.answer('Computing...')  # a temporary message that will be deleted

    

    translated_text, l = translate(text, 'en')
    spok_resp, wolfram_not_understand = spok_resp_get(translated_text)
    count = 0
    if wolfram_not_understand:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + a, 
                                    text='Wolfram|Alpha did not understand your input, but we will now ask ChatGPT.')
        while wolfram_not_understand and count < 3:
            g4f_resp = g4f_convert(translated_text)
            query = g4f_resp[g4f_resp.find('`')+1:g4f_resp.rfind('`')]
            spok_resp, wolfram_not_understand = spok_resp_get(query)
            count += 1
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + a, 
                                    text='Wolfram|Alpha did not understand your input, but we will now ask ChatGPT' + '.'*(count+1))
        else:
            t = 'ChatGPT was able to convert the request. Ask Wolfram Alpha' if not(wolfram_not_understand) else 'Didn\'t get your request converted. The ChatGPT response will now be displayed'
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + a, text=t)
    else:
        g4f_resp = 'https'
        query = translated_text
    
    if wolfram_not_understand:
        step_resp = False
        simp_resp = False
    else:
        quote_query = requests.utils.requote_uri(query) # replace spaces and other special characters with their encoded values

        simp_resp = f'https://api.wolframalpha.com/v1/simple?appid={simple_api}&i={quote_query}%3F'
        simp_file_name = str(id) + 'simp.png'
        step_file_name = str(id)
        simp_resp = download_image(simp_resp, simp_file_name)
        step_resp = step_by_step_response(quote_query, str(id))

        if spok_resp == 'No spoken result available':
            spok_resp = '' 
        else:
            spok_resp = translate(spok_resp, l)[0]



    try:
        if step_resp:  # If a step-by-step solution is in place
            photo_list = [InputMediaPhoto(media=FSInputFile(simp_file_name), caption=spok_resp)]
            for i in step_resp:
                photo_list.append(InputMediaPhoto(media=FSInputFile(i)))
            await bot.send_media_group(chat_id=message.chat.id, media=photo_list, request_timeout=10)
            
            os.remove(simp_file_name)
            for i in range(len(step_resp)):
                os.remove(f"{step_file_name}_{i + 1}.png")

        elif simp_resp:
            await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(simp_file_name), caption=spok_resp, request_timeout=10)
            os.remove(simp_file_name)

        elif not(wolfram_not_understand) and spok_resp != '':
            await message.answer(spok_resp)

        elif 'https' not in g4f_resp:
            await message.answer(translate(g4f_resp, l)[0])

        else:
            await message.answer('Wolfram|Alpha did not understand your input')

    except Exception as e:
        print('Message: ', e)
        await message.answer(text=f'{spok_resp}\n'
                            f' Error. Most likely, the admin is changing something. Wait a few minutes.')

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + a)
    sql_message(text, message.from_user.full_name, message.from_user.username, message.from_user.id, add)



if __name__ == '__main__':
    sql_launch()
    dp.run_polling(bot, skip_updates=True)
