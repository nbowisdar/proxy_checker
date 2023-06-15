from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import aiogram.types as t
from app.structure.models import Proxy, Site
from app import utils


drop_msg = t.InlineKeyboardButton(text="↙️ Приховати", callback_data="hide")

cancel_kb = t.ReplyKeyboardMarkup(
    keyboard=[[t.KeyboardButton(text="🛑 Скасувати")]], resize_keyboard=True
)


admin_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👤 Проксі"),
            KeyboardButton(text="📊 Статистика"),
        ],
    ],
    resize_keyboard=True,
)


def change_proxy_inl(proxy_id) -> t.InlineKeyboardMarkup:
    return t.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                t.InlineKeyboardButton(
                    text="♻️ Оновити", callback_data=f"change_proxy|update|{proxy_id}"
                ),
                t.InlineKeyboardButton(
                    text="🗑 Видалити", callback_data=f"change_proxy|delete|{proxy_id}"
                ),
            ],
            [drop_msg],  # noqa: F405
        ]
    )


def get_proxy_variants_kb() -> t.InlineKeyboardButton:
    builder = InlineKeyboardBuilder()
    for proxy_name, status in Proxy.get_proxy_status():
        show_name = f"{proxy_name.capitalize()} {utils.get_status_symbol(status)}"
        builder.row(
            t.InlineKeyboardButton(text=show_name, callback_data=f"proxy|{proxy_name}")
        )
    return builder.as_markup()


statistick_btn = t.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            t.InlineKeyboardButton(text="🔰 За добу", callback_data="error_stat|day"),
            t.InlineKeyboardButton(
                text="⌚️ За неділю", callback_data="error_stat|week"
            ),
        ],
        [
            t.InlineKeyboardButton(
                text="🗓 За місяць", callback_data="error_stat|month"
            ),
            t.InlineKeyboardButton(
                text="🌎 За 3 місяці", callback_data="error_stat|3months"
            ),
            # t.InlineKeyboardButton(
            #     text="📊 Уся статистика", callback_data="new_user_stat|all_new_user_stat"
            # ),
        ],
        [drop_msg],
    ]
)
