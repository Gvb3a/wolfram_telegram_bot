# WolframAlpha telegram bot
This telegram bot uses the [WolframAlpha API](https://products.wolframalpha.com/api/faqs) to answer queries. There is also image recognition with the help of a free analogue of Mathpix - [SimpleTex](https://www.simpletex.net/).There is also a translator and you can write in any language. Written in aiogram.
## Usage
All api changes take place in `config.py`. First get the WolframAlpha api. Go to [deloper portal](https://developer.wolframalpha.com/access), register and click on Get an App ID. You choose a name and description and select Simple API first, then Show Steps API (two will be enough). Then open `config.py` and assign spoken_api and simple_api value (token) to the received Simple API, and for show_steps_api and llm_api value to Show Steps API.
get bot_token from [BotFather](https://t.me/BotFather) (there you create a bot).
simple_tex_api is needed for recognising pictures. I used [SimpleTex](https://www.simpletex.net/), because [mathpix api](https://docs.mathpix.com/#introduction) is paid. Also pass registration, then [API](https://www.simpletex.net/api)>[Go to API Dashboard](https://simpletex.net/user/center?menu=oapi)>User Access Token>Create New Token. 
I also added translation of requests and answers, which is very convenient for people who speak non-English. api for translator is not needed, but you need api for language detection. Register [there](https://detectlanguage.com/users/sign_up) get the api and paste it into detect_language_api
All api are free

To run the bot itself, download the necessary libraries and run `main.py`

## Todo
- [ ] Examples of api usage
- [ ] Help message (example, text.md)
- [ ] Site (maybe with streamlit)
- [ ] random walk (limitations, animation)
- [ ] Translating a message in text mode
