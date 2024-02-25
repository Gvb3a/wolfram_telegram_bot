from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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
