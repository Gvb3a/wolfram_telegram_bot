import requests
from datetime import datetime  # just to display the time of request or error
from urllib.parse import quote  # is used to replace spaces and other special characters with their encoded values
from bs4 import BeautifulSoup
from config import spoken_api, simple_api, show_steps_api, llm_api


def wolfram_step_by_step_response(query):
    url = f'https://api.wolframalpha.com/v1/query?appid={show_steps_api}&input=solve+{query}&podstate=Step-by-step%20solution'

    try:
        soup = BeautifulSoup(requests.get(url).content, "xml")
        subpod = soup.find("subpod", {"title": "Possible intermediate steps"})
        img_tag = subpod.find("img")
        return img_tag.get("src") if img_tag else False
    except:
        return False


def main_wolfram(query):
    print(f'\nEnquiry: {query}. time: {datetime.now().strftime("%H:%M:%S")}')
    query = quote(query)

    spok_resp = requests.get(f'https://api.wolframalpha.com/v1/spoken?appid={spoken_api}&i={query}').text
    simp_resp = f'https://api.wolframalpha.com/v1/simple?appid={simple_api}&i={query}%3F'
    # llm_resp = requests.get(f'https://api.wolframalpha.com/v1/llm-api?input={query}&appid={llm_api}').text

    step_resp = wolfram_step_by_step_response(query)

    print(spok_resp, simp_resp, step_resp, datetime.now().strftime("%H:%M:%S"))
    return [spok_resp, simp_resp, step_resp]