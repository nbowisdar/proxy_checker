from pprint import pprint
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Text, Command
from aiogram import F
from ..models import Proxy
from setup import admin_router
from app.handlers.fsm_h.block_user import BlockUser, UnblockUser
import aiogram.types as t
from app.buttons import admin_btns as kb
from app import crud
from aiogram.fsm.state import State, StatesGroup


@admin_router.message(F.text.in_(["🛑 Скасувати", "↩️ Назад"]))
async def cancel_handler(message: t.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Головна", reply_markup=kb.admin_main_kb)
        return
    await state.clear()
    await message.answer("🛑 Скасованно", reply_markup=kb.admin_main_kb)


@admin_router.callback_query(F.text == "hide")
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
    await message.answer("stat")


class AddProxy(StatesGroup):
    name = State()
    address = State()
    port = State()
    login = State()
    password = State()


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
        await callback.message.edit_text("update / delete proxy")


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
        await message.reply("Повинно бути число", reply_markup=kb.admin_main_kb)
        await state.clear()
    await state.update_data(port=port)
    await state.set_state(AddProxy.login)
    await message.reply("Відправте логін")


@admin_router.message(AddProxy.login)
async def add_username(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await state.set_state(AddProxy.password)
    await message.reply("Відправте пароль")


@admin_router.message(AddProxy.password)
async def add_passwd(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    await state.clear()
    proxy = Proxy.create(**data)
    await message.reply("✅ Ви додали нову проксі", reply_markup=kb.admin_main_kb)


@admin_router.message(F.text == "")
async def update_proxy(message: Message, state: FSMContext):
    pass


@admin_router.message(F.text == "")
async def update_proxy(message: Message, state: FSMContext):
    pass


@admin_router.message(F.text == "")
async def update_proxy(message: Message, state: FSMContext):
    pass
