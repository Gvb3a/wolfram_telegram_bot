# WolframAlpha telegram bot
Telegram bot with using [WolframAlpha API](https://products.wolframalpha.com/api/faqs). Written on [aiogram](https://docs.aiogram.dev/en/latest/). Try [here](https://t.me/wolfram_mp_bot)

## Api
Before launching the bot, create an `.env` file and populate it with the following API (all API are free)
```
BOT_TOKEN=
SIMPLE_API=
SHOW_STEP_API=
SIMPLE_TEX_API=
DETECT_LANGUAGE_API=
GENAI_API_KEY=
```
* `BOT_TOKEN` - API for bot telegram. To get it you need to create a bot in [BotFather](https://t.me/BotFather)
* `WOLFRAM_SIMPLE_API` - WolframAlpha API for [Simple API](https://products.wolframalpha.com/simple-api/documentation) and [Spoken Results API](https://products.wolframalpha.com/spoken-results-api/documentation)
* `WOLFRAM_SHOW_STEP_API` - WolframAlpha API for [Show Steps API](https://products.wolframalpha.com/show-steps-api/documentation)
* `SIMPLE_TEX_API` - the API of the Chinese analog of [Mathpix](https://mathpix.com/). Get it from [site](https://simpletex.net/api)
* `DETECT_LANGUAGE_API` - Even though translation is done through [deep_translator](https://pypi.org/project/deep-translator/) and does not require an API, I use [Detect Language API](https://detectlanguage.com/) to save the user's language and translate responses
* `DETECT_LANGUAGE_API` - Gemini. Gives the ability to recognize photos much better and also to formulate queries if the user has entered an unclear query. [Google studio](https://aistudio.google.com/app/apikey)
## Todo
- [ ] Comment and clean up the code 
- [ ] Statistics
- [ ] Improve interaction with the database
- [ ] Improve random walk
