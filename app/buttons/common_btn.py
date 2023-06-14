import aiogram.types as t


drop_msg = t.InlineKeyboardButton(text="↙️ Приховати", callback_data="hide")

cancel_kb = t.ReplyKeyboardMarkup(
    keyboard=[[t.KeyboardButton(text="🛑 Скасувати")]], resize_keyboard=True
)


# cancel = t.InlineKeyboardButton(text="🛑 Cancel", callback_data="ai_cancel")
#
# cancel_inl = t.InlineKeyboardMarkup(inline_keyboard=[[cancel]])
