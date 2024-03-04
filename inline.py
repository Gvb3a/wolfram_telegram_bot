from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

help_message = ('This telegram bot works with Wolfram|Alpha. Wolfram|Alpha provides '
                'answers not by searching the Internet, but by performing dynamic computations based on a huge '
                'collection of built-in data, algorithms and methods. In the future, there will be an additional '
                'manual on mathematics and programming languages.\n'
                '\nIf Wolfram|Alpha does not understand you, try the following:\n'
                'Use different phrasing or notations\nEnter whole words instead of abbreviations\n'
                'Avoid mixing mathematical and other notations\nCheck your spelling\nGive your input in English\n'
                '\nOther tips for using Wolfram|Alpha:\nWolfram|Alpha answers specific questions rather than '
                'explaining general topics(e.g. Enter "2 cups of sugar", not "nutrition information")\n'
                'You can only get answers about objective facts(e.g. Try "highest mountain", not "most beautiful '
                'painting")\nOnly what is known is known to Wolfram|Alpha (e.g. Ask "how many men in Mauritania", '
                'not "how many monsters in Loch Ness")\nOnly public information is available (e.g. Request '
                '"GDP of France", not "home phone of Michael Jordan")\n\nExamples by Topic:')

inline_help_Mathematics = InlineKeyboardButton(
    text='Example: Mathematics',
    callback_data='help>Mathematics'
)
math_example = ('Mathematics\nWolfram|Alpha has broad knowledge and deep computational power when it '
                'comes to math. Whether it be arithmetic, algebra, calculus, differential equations or anything in '
                'between, Wolfram|Alpha is up to the challenge. Get help with math homework, solve specific math '
                'problems or find information on mathematical subjects and topics.\n\nElementary Math: 125 + 375; '
                'sqrt (3^2 + 4^2); (2*3 + 3*4 + 4*5) / (10 - 5); 135/216 - 12/25; 30% of 8 miles; '
                'round (56.824, 10); place values 28.75; 1 + (even number * odd number); Rachel has 17 apples. '
                'She gives 9 to Sarah. How many apples does Rachel have now?\n\nAlgebra: solve x^2 + 4x - 5 = 0;'
                'x+y=10, x-y=4; factor 2x^5 - 19x^4 + 58x^3 - 67x^2 + 56x - 48; (x^2-1)/(x^2+1); quaternion: 0+2i-j-3k;'
                ' perm (1 2 3 4)^3(1 2 3)^-1; domain of f(x) = x/(x^2-1); compute the area between y=|x| and y=x^2-6;'
                '1, 4, 9, 16, 25, ...; 3 + 12 + 27 + ... + 300; derivative of x^4 sin x\n\nGeometry: Reuleaux triangle;'
                'pack 24 circles in a circle; How many baseballs fit in a Boeing 747?; golden ratio with side 1=2m;'
                'hexagon, perimeter=100; dodecahedron\n\nPlotting & Graphics: plot x^3 - 6x^2 + 4x + 12; plot '
                'sin x cos y; number line 2, 3, 5, 7, 11, 13; plot sin x, cos x, tan x; polar plot r=1+cos theta\n\n'
                'Numbers: 28; pi to 1000 digits; golden ratio - 1/(golden ratio); XLVIII + LXXII; 49 tredecillion;'
                'negative integer / positive integer;\n\nTrigonometry: sin(pi/5); plot sin(x); sin x + cos x = 1;'
                'closed-form values of tan(x); law of cosines; law of haversines\n\nLinear Algebra: {1/4, -1/2, 1} '
                'cross {1/3, 1, -2/3}; {{2, -1}, {1, 3}} . {{1, 2}, {3, 4}}; {{1, 0, -1}, {2, -1, 3}} column space\n\n'
                'Number Theory: 1,000,000th prime; divisors 3600; solve 3x+4y=5 over the integers; add up the digits '
                'of 2567345; 20 greatest triangular numbers < 500; 7 rows of Pascal\'s triangle; primes <= 100\n\n'
                'Discrete Mathematics: 12! / (4! * 6! * 2!); odd partitions of 14; number of partitions of 1250; '
                '6x6 Latin squares; fixed necklaces with 6 beads and 3 colors; Pappus graph; binary tree; Petersen '
                'graph\n\nApplied Mathematics: maximize 5 + 3x - 4y - x^2 + x y - y^2; Julia set -0.40+0.65i; '
                'Mandelbrot set; tic-tac-toe game; rock-scissors-paper game\n\nContinued Fractions: continued fraction '
                'pi; continued fraction tan x; common notations for continued fractions; apply continued fraction '
                'theorems to sqrt(7)\n\nStatistics: {25, 35, 10, 17, 29, 14, 21, 31}; mean {21.3, 38.4, 12.7, 41.6}\n\n'
                'Probability: 32 coin tosses; 5 dice; 8:5 odds, bet 97 euros; streak of 12 successes in 40 trials; '
                'number of trials until 15th success; birthday paradox 50 people\n\n\n'
                'And that\'s just a drop in the ocean. I didn\'t understand most of the examples, so if you\'re a maths'
                ' student, I suggest you dive into this vast sea. https://www.wolframalpha.com/examples/mathematics')

inline_help_ScienceTechnology = InlineKeyboardButton(
    text='Example: Science & Technology',
    callback_data='help>ScienceTechnology'
)
inline_help_SocietyCulture = InlineKeyboardButton(
    text='Example: Society & Culture',
    callback_data='help>SocietyCulture'
)
inline_help_EverydayLife = InlineKeyboardButton(
    text='Example: Everyday Life',
    callback_data='help>EverydayLife'
)
help_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[inline_help_Mathematics],
                     [inline_help_ScienceTechnology],
                     [inline_help_SocietyCulture],
                     [inline_help_EverydayLife]]
)
inline_help_back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text='Back',
    callback_data='help>back'
)]])

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
