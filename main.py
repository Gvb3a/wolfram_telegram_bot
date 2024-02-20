import asyncio
import requests

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InputMediaPhoto, Message
from urllib.parse import quote  # is used to replace spaces and other special characters with their encoded values
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
from colorama import Fore, Style

from config import *


bot = Bot(bot_token)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(text=f"Hello, {message.from_user.full_name}! Enter what you want to calculate or know about")
    print(f'{Fore.RED}/start{Style.RESET_ALL} comand from {Fore.BLUE}{message.from_user.full_name}{Style.RESET_ALL} '
          f'at {datetime.now().strftime("%H:%M:%S")}')


@dp.message(Command('help'))
async def command_help(message: Message) -> None:
    await message.answer('help message(in development)')
    print(f'{Fore.RED}/help{Style.RESET_ALL} comand from {Fore.BLUE}{message.from_user.full_name}{Style.RESET_ALL} '
          f'at {datetime.now().strftime("%H:%M:%S")}')


mode = True

@dp.message(Command('mode'))
async def comand_mode(message: Message) -> None:
    global mode
    mode = not mode

    if mode:
        await message.answer(text='Mode changed to text')
    else:
        await message.answer(text='Mode changed to pictures')
    print(f'User {Fore.BLUE}{message.from_user.full_name}{Style.RESET_ALL} changed the mode to '
          f'{Fore.RED}{mode}{Style.RESET_ALL} at {datetime.now().strftime("%H:%M:%S")}')
    

def step_by_step_response(query):
    if mode:
        url = f'https://api.wolframalpha.com/v1/query?appid={show_steps_api}&input=solve+{query}&podstate=Step-by-step%20solution'

        try:
            soup = BeautifulSoup(requests.get(url).content, "xml")
            subpod = soup.find("subpod", {"title": "Possible intermediate steps"})
            img_tag = subpod.find("img")
            return img_tag.get("src") if img_tag else False
        except:
            return False
    else:
        pass


@dp.message()
async def wolfram(message: types.Message) -> None:
    await message.answer('Calculate...')
    print(f'Request {Fore.GREEN}{message.text}{Style.RESET_ALL} from '
          f'{Fore.BLUE}{message.from_user.full_name}{Style.RESET_ALL} at {datetime.now().strftime("%H:%M:%S")}')
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
                
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
    print(f'A reply to the {Fore.GREEN}{message.text}{Style.RESET_ALL} was sent to '
              f'{Fore.BLUE}{message.from_user.full_name}{Style.RESET_ALL} at {datetime.now().strftime("%H:%M:%S")}')
    else:
        pass


if __name__ == '__main__':

    print(f'The bot {Fore.RED}launches{Style.RESET_ALL} at {datetime.now().strftime("%H:%M:%S %d.%m.%Y")}')

    async def main():
        await dp.start_polling(bot)


    asyncio.run(main())
