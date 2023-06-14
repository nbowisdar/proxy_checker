from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import aiogram.types as t
from setup import periods

drop_msg = t.InlineKeyboardButton(text="↙️ Приховати", callback_data="hide")

_cancel = t.KeyboardButton(text="🔴 Скасувати")

cancel_kb = t.ReplyKeyboardMarkup(
    keyboard=[[t.KeyboardButton(text="🔴 Скасувати")]], resize_keyboard=True
)


user_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Додати сайт"),
            KeyboardButton(text="📜 Усі сайти"),
        ],
        [KeyboardButton(text="✍️ Зв'язок з адміністрацією")],
    ],
    resize_keyboard=True,
)


def get_period_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for per in periods.keys():
        builder.add(t.KeyboardButton(text=per))
    builder.row(_cancel)
    return builder.as_markup(resize_keyboard=True)
