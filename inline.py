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
math_example = ('Mathematics\n'
                'Wolfram|Alpha has broad knowledge and deep computational power when it comes to math. Whether it be '
                'arithmetic, algebra, calculus, differential equations or anything in between, Wolfram|Alpha is up to '
                'the challenge. Get help with math homework, solve specific math problems or find information on '
                'mathematical subjects and topics.\n\n'
                'Elementary Math: 125 + 375; sqrt (3^2 + 4^2); (2*3 + 3*4 + 4*5) / (10 - 5); 135/216 - 12/25; '
                '30% of 8 miles; round (56.824, 10); place values 28.75; 1 + (even number * odd number); Rachel has '
                '17 apples. She gives 9 to Sarah. How many apples does Rachel have now?\n\n'
                'Algebra: solve x^2 + 4x - 5 = 0; x+y=10, x-y=4; factor 2x^5 - 19x^4 + 58x^3 - 67x^2 + 56x - 48;'
                '(x^2-1)/(x^2+1); quaternion: 0+2i-j-3k; perm (1 2 3 4)^3(1 2 3)^-1; domain of f(x) = x/(x^2-1);'
                'compute the area between y=|x| and y=x^2-6; 1, 4, 9, 16, 25, ...; 3 + 12 + 27 + ... + 300; '
                'derivative of x^4 sin x\n\n'
                'Geometry: Reuleaux triangle; pack 24 circles in a circle; How many baseballs fit in a Boeing 747?; '
                'golden ratio with side 1=2m; hexagon, perimeter=100; dodecahedron\n\n'
                'Plotting & Graphics: plot x^3 - 6x^2 + 4x + 12; plot  sin x cos y; number line 2, 3, 5, 7, 11, 13;'
                'plot sin x, cos x, tan x; polar plot r=1+cos theta\n\n'
                'Numbers: 28; pi to 1000 digits; golden ratio - 1/(golden ratio); XLVIII + LXXII; 49 tredecillion;'
                'negative integer / positive integer;\n\n'
                'Trigonometry: sin(pi/5); plot sin(x); sin x + cos x = 1; closed-form values of tan(x);'
                'law of cosines; law of haversines\n\n'
                'Linear Algebra: {1/4, -1/2, 1} cross {1/3, 1, -2/3}; {{2, -1}, {1, 3}} . {{1, 2}, {3, 4}};'
                '{{1, 0, -1}, {2, -1, 3}} column space\n\n'
                'Number Theory: 1,000,000th prime; divisors 3600; solve 3x+4y=5 over the integers; add up the digits '
                'of 2567345; 20 greatest triangular numbers < 500; 7 rows of Pascal\'s triangle; primes <= 100\n\n'
                'Discrete Mathematics: 12! / (4! * 6! * 2!); odd partitions of 14; number of partitions of 1250; '
                '6x6 Latin squares; fixed necklaces with 6 beads and 3 colors; Pappus graph; binary tree; Petersen '
                'graph\n\n'
                'Applied Mathematics: maximize 5 + 3x - 4y - x^2 + x y - y^2; Julia set -0.40+0.65i; Mandelbrot set; '
                'tic-tac-toe game; rock-scissors-paper game\n\n'
                'Continued Fractions: continued fraction pi; continued fraction tan x; common notations for continued '
                'fractions; apply continued fraction theorems to sqrt(7)\n\n'
                'Statistics: {25, 35, 10, 17, 29, 14, 21, 31}; mean {21.3, 38.4, 12.7, 41.6}\n\n'
                'Probability: 32 coin tosses; 5 dice; 8:5 odds, bet 97 euros; streak of 12 successes in 40 trials; '
                'number of trials until 15th success; birthday paradox 50 people\n\n\n'
                'And that\'s just a drop in the ocean. I didn\'t understand most of the examples, so if you\'re a maths'
                ' student, I insist on diving into this vast sea of. https://www.wolframalpha.com/examples/mathematics')

inline_help_ScienceTechnology = InlineKeyboardButton(
    text='Example: Science & Technology',
    url='https://www.wolframalpha.com/examples/science-and-technology'
)
Science_example = ("Wolfram|Alpha has extensive knowledge related to science and technology. Using the computational "
                   "power behind Wolfram|Alpha, solve problems involving physics, chemistry, engineering, "
                   "computational sciences and many other domains.\n\n"
                   "Physics: mechanical advantage of a lever, effort arm: 1m, load arm: 20 cm, lever type: first class;"
                   "work at constant acceleration, d = 1m, m = 1 kg, a = 1 m/s^2; mechanical work, 30 degrees, "
                   "F = 1 N, d = 1 m; Coriolis effect 5mph 30rpm; a 2.1kg block slides down an inclined plane, "
                   "slope angle: 34 °, static friction coefficient: 0.6, kinetic friction coefficient: 0.4, "
                   "initial velocity: 0 m/s, time: 3 s; F=5 Newtons, t=8 seconds; rolling motion, v=3m/s, "
                   "omega=40 rad/s, m=1 kg, moment of inertia = 0.01 kg m^2; pulley system, n=4; small oscillation "
                   "pendulum, length=.5 m, initial angle=20°, g=1 g; free particle; elastic collision m1=3kg, v1i=4m/s,"
                   " m2=2kg, v2i=-1m/s; 2d elastic collision, theta=40deg, mass 1=1 kg, mass 2=1 kg, "
                   "initial speed 1=1 m/s; two-body problem; time to fall 1000ft; massive cube; diameter 5mm and force "
                   "2N, what is the mechanical stress; Hamiltonian p^2/2 - cos(q); pendulum (physical system); "
                   "play sin(3000t)+sin(4243t); msd for neon at 800 K, thermal speed m=28 u, T=20C; random walk in 1D,"
                   " 100 steps; 2D random walk, 1000 steps; 3D random walk, 500 steps; Wien's law, T = 5780 K, "
                   "trimethylamine gas, 2,3-methano-5,6-dichloroindene"
                   "")
inline_help_SocietyCulture = InlineKeyboardButton(
    text='Example: Society & Culture',
    url='https://www.wolframalpha.com/examples/society-and-culture'
)
inline_help_EverydayLife = InlineKeyboardButton(
    text='Example: Everyday Life',
    url='https://www.wolframalpha.com/examples/everyday-life'
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
