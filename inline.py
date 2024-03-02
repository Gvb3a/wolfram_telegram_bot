from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

help_message = ('This telegram bot works with Wolfram|Alpha. Wolfram|Alpha provides answers not by searching the '
                'Internet, but by performing dynamic computations based on a huge collection of built-in data, '
                'algorithms and methods. In the future, there will be an additional manual on mathematics and '
                'programming languages.\n'
                '\nIf Wolfram|Alpha does not understand you, try the following:\n'
                'Use different phrasing or notations\nEnter whole words instead of abbreviations\n'
                'Avoid mixing mathematical and other notations\nCheck your spelling\nGive your input in English\n'
                '\nOther tips for using Wolfram|Alpha:\nWolfram|Alpha answers specific questions rather than '
                'explaining general topics(e.g. Enter "2 cups of sugar", not "nutrition information")\n'
                'You can only get answers about objective facts(e.g. Try "highest mountain", not "most beautiful '
                'painting")\nOnly what is known is known to Wolfram|Alpha (e.g. Ask "how many men in Mauritania", '
                'not "how many monsters in Loch Ness")\nOnly public information is available (e.g. Request '
                '"GDP of France", not "home phone of Michael Jordan")\n'
                '\nExamples:\n'
                'solve x^2 + 4x + 6 = 0\nx^2+y^2=1, (x-2)^2+(y-1)^2=4\nusing Newton\'s method solve x cos x = 0\n'
                'factor 2x^5 - 19x^4 + 58x^3 - 67x^2 + 56x - 48\nrational solutions of x^3 - 3x + 2\n'
                'quaternion: 0+2i-j-3k\ndomain of f(x) = x/(x^2-1)\n15% off of $29.95\n'
                'Rachel has 17 apples. She gives 9 to Sarah. How many apples does Rachel have now?\n'
                '1 + (even number * odd number)\nnegative number ^ 40\ntrefoil knot\n'
                '3d parametric plot (cos t, sin 2t, sin 3t)\n1, 4, 9, 16, 25, ...\nmean {21.3, 38.4, 12.7, 41.6}'
                '\n1/2 + 1/4 + 1/8 + 1/16 + ...\nis y=x^3+x a one-to-one function?\n Riemann Hypothesis\nfactor 70560'
                '\nsin(pi/5)\nnumber of trials until 15th success\nstreak of 12 successes in 40 trials\n'
                'probability of 3rd head on 8th flip\nrule 110\ntotal length of all roads in Spain\n'
                'Am I too drunk to drive?\nworld gdp per capita\nearthquakes June 2006\n'
                'Albert Einstein, Paul Dirac, Richard Feynman\nterminator 2\nMDCCLXXVI\nCanada healthcare expenditures'
                'obfuscate 42\n1 + 2 + 3 + 4 + ...\npi day\ngraph sin t + cos (sqrt(3)t) handwritten style')

inline_geometry = InlineKeyboardButton(
    text='Geometry',
    callback_data='theory>geometry'
)
inline_algebra = InlineKeyboardButton(
    text='Algebra',
    callback_data='theory>algebra'
)
inline_python = InlineKeyboardButton(
    text='Python',
    callback_data='theory>python'
)
inline_close = InlineKeyboardButton(
    text='Close',
    callback_data='theory>close'
)
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[inline_geometry],
                     [inline_algebra],
                     [inline_python],
                     [inline_close]]
)

# theory>geometry
inline_geometry_triangleArea = InlineKeyboardButton(
    text='Triangle area',
    callback_data='theory>geometry>triangleArea'
)
inline_geometry_back = InlineKeyboardButton(
    text='Back',
    callback_data='theory>geometry>back'
)
keyboard_geometry = InlineKeyboardMarkup(
    inline_keyboard=[[inline_geometry_triangleArea],
                     [inline_geometry_back]]
)
