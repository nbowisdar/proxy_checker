from pprint import pprint
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Text, Command
from aiogram import F
from loguru import logger
from ..structure.models import Proxy
from setup import admin_router
from app.handlers.fsm_h.block_user import BlockUser, UnblockUser
import aiogram.types as t
from app.buttons import admin_btns as kb
from app import crud
from aiogram.fsm.state import State, StatesGroup
from app import msgs, utils
from app.structure.schemas import per_by_name


@admin_router.message(F.text.in_(["🛑 Скасувати", "↩️ Назад"]))
async def cancel_handler(message: t.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Головна", reply_markup=kb.admin_main_kb)
        return
    await state.clear()
    await message.answer("🛑 Скасованно", reply_markup=kb.admin_main_kb)


@admin_router.callback_query(Text("hide"))
async def anon(callback: t.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.clear()
    await callback.message.delete()


@admin_router.message(Command(commands="admin"))
async def test(message: Message):
    await message.answer("Головна", reply_markup=kb.admin_main_kb)


@admin_router.message(F.text == "👤 Проксі")
async def proxy(message: Message):
    await message.answer("proxy", reply_markup=kb.get_proxy_variants_kb())


@admin_router.message(F.text == "📊 Статистика")
async def stat(message: Message):
    await message.answer("📊 Статистика", reply_markup=kb.statistick_btn)


@admin_router.callback_query(Text(startswith="error_stat"))
async def hendle_proxy(callback: t.CallbackQuery):
    await callback.message.delete()
    _, period_str = callback.data.split("|")
    period = per_by_name[period_str]
    errors = crud.get_errs_by_period(period)
    # limit_errors = crud.get_one_res_per_day(errors)

    big_msg = msgs.build_error_statistic(errors)
    if big_msg:
        for msg in utils.divide_big_msg(big_msg):
            if msg:
                await callback.message.answer(msg)
    else:
        await callback.message.answer("Поки що немає статистики")


class AddProxy(StatesGroup):
    name = State()
    address = State()
    port = State()
    login = State()
    password = State()


class UpdateProxy(StatesGroup):
    proxy_id = State()
    proxy = State()


@admin_router.callback_query(Text(startswith="proxy"))
async def hendle_proxy(callback: t.CallbackQuery, state: FSMContext):
    _, proxy_name = callback.data.split("|")
    proxy = crud.get_proxy_by_name(proxy_name)
    if not proxy:
        await state.update_data(name=proxy_name)
        await callback.message.delete()
        await callback.message.answer("Відправте адрес.", reply_markup=kb.cancel_kb)

        await state.set_state(AddProxy.address)
    else:
        # await callback.message.edit_text("update / delete proxy")
        # _, proxy_name = callback.data.split("|")
        proxy: Proxy = crud.get_proxy_by_name(proxy_name)
        proxy_msg = msgs.build_proxy_msg(proxy)
        await callback.message.edit_text(
            proxy_msg, reply_markup=kb.change_proxy_inl(proxy.id)
        )


@admin_router.callback_query(Text(startswith="change_proxy"))
async def change_proxy(callback: t.CallbackQuery, state: FSMContext):
    _, action, proxy_id = callback.data.split("|")
    await callback.message.delete()
    if action == "delete":
        Proxy.delete().where(Proxy.id == int(proxy_id)).execute()
        await callback.message.answer("🗑 Видаленно", reply_markup=kb.admin_main_kb)

    elif action == "update":
        await state.set_state(UpdateProxy.proxy)
        await state.update_data(proxy_id=proxy_id)
        await callback.message.answer(
            "Відправте проксі в форматі:\n*address:port:login:password*",
            reply_markup=kb.cancel_kb,
        )


@admin_router.message(UpdateProxy.proxy)
async def update_proxy(message: Message, state: FSMContext):
    data = await state.get_data()
    proxy: Proxy = Proxy.get_by_id(data["proxy_id"])
    try:
        addr, port, login, password = message.text.split(":")
        proxy.address = addr
        proxy.port = int(port)
        proxy.login = login
        proxy.password = password
    except ValueError:
        await message.reply("❌ Не вірний формат!", reply_markup=kb.admin_main_kb)
        await state.clear()
        return

    if await utils.check_proxy(proxy):
        proxy.save()
        msg = "✅ Проксі оновленно"
    else:
        msg = "❌ Не можу з'єднатися з сервером."
    await message.reply(msg, reply_markup=kb.admin_main_kb)


@admin_router.message(AddProxy.address)
async def add_addr(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(AddProxy.port)
    await message.reply("Відправте порт")


@admin_router.message(AddProxy.port)
async def add_port(message: Message, state: FSMContext):
    try:
        port = int(message.text)
    except ValueError:
        await message.answer("❌ Повинно бути число", reply_markup=kb.admin_main_kb)
        await state.clear()
        return
    await state.update_data(port=port)
    await state.set_state(AddProxy.login)
    await message.answer("Відправте логін")


@admin_router.message(AddProxy.login)
async def add_username(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await state.set_state(AddProxy.password)
    await message.answer("Відправте пароль")


@admin_router.message(AddProxy.password)
async def add_passwd(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    await state.clear()
    proxy: Proxy = Proxy.create(**data)
    msg_sent = await message.answer("⌛ Перевірка проксі...")
    if await utils.check_proxy(proxy):
        msg = "✅ Ви додали нову проксі\n" + msgs.build_proxy_msg(proxy)
    else:
        msg = "❌ Не можу з'єднатися з сервером."
        proxy.delete_instance()
    await msg_sent.delete()
    await message.answer(msg, reply_markup=kb.admin_main_kb)


# @admin_router.message(F.text == "")
# async def update_proxy(message: Message, state: FSMContext):
#     pass


# @admin_router.message(F.text == "")
# async def update_proxy(message: Message, state: FSMContext):
#     pass


# @admin_router.message(F.text == "")
# async def update_proxy(message: Message, state: FSMContext):
#     pass
