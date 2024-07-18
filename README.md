# WolframAlpha telegram bot
This telegram bot uses [WolframAlpha API](https://products.wolframalpha.com/api/faqs) to answer queries.  There is image recognition using the free Mathpix analog [SimpleTex](https://www.simpletex.net/). There is also a translator that helps to write a query in any language. The bot is written by [aiogram](https://docs.aiogram.dev/en/latest/)

## Api
All API are stored in .env. Each of the APIs is completely free and easy to get.
- BOT_TOKEN. This is the API for Telegram. Go to [BotFather](https://t.me/BotFather), create a bot and get a token.
- SIMPLE_API and SHOW_STEP_API. The bots brain (WolframAlpha). Go to [developer portal](https://developer.wolframalpha.com/), register and click on "Get an App ID". There you will get two APIs: [Simple API](https://products.wolframalpha.com/simple-api/documentation) and [Show Steps API](https://products.wolframalpha.com/show-steps-api/documentation). Wolfram offers 2000 free calls per month! That's enough for everything.
- SIMPLE_TEX_API. Allows to convert photo to LaTeX. Was planning to do it with [Mathpix](https://mathpix.com/), but it's paid, so I'm using [SimpleTex](https://simpletex.net/). Receipt path: [API Dashboard](https://simpletex.net/user/center?menu=oapi) >>> register >>> User Access Token >>> Create New Token
- DETECT_LANGUAGE_API. This API is needed for the translator. The translation itself is done through [deep_translator](https://pypi.org/project/deep-translator/) which does not require an api for translation, but it takes a very long time to detect the language itself in something like this: "3x-1=11". So for optimisation I use the API that detects the language. Go to [Detect Language API](https://detectlanguage.com/), click on 'Get API key' and register.

## Todo
- [ ] Comment the code normally
- [ ] Make normal statistics
- [ ] Maybe do something with random walk
