from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import aiogram.types as t
from app.models import Proxy, Site
from app import utils

# from app import crud
from .common_btn import *

admin_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👤 Проксі"),
            KeyboardButton(text="📊 Статистика"),
        ],
    ],
    resize_keyboard=True,
)


def get_proxy_variants_kb() -> t.InlineKeyboardButton:
    builder = InlineKeyboardBuilder()
    for proxy_name, status in Proxy.get_proxy_status():
        show_name = f"{proxy_name.capitalize()} {utils.get_status_symbol(status)}"
        builder.row(
            t.InlineKeyboardButton(text=show_name, callback_data=f"proxy|{proxy_name}")
        )
    return builder.as_markup()
