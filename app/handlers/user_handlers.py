from pprint import pprint
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Text, Command
from aiogram import F
from app.structure.models import User, Site
from setup import periods

from setup import user_router
from app.handlers.fsm_h.block_user import BlockUser, UnblockUser
import aiogram.types as t
from app.buttons import user_btn as kb
from app import crud
from aiogram.fsm.state import State, StatesGroup
from app import msgs, utils


@user_router.message(F.text.in_(["🔴 Скасувати", "↩️ Назад"]))
async def cancel_handler(message: t.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("🏡 Головна", reply_markup=kb.user_main_kb)
        return
    await state.clear()
    await message.answer("🔴 Скасованно", reply_markup=kb.user_main_kb)


@user_router.message(Command(commands="start"))
async def main(message: Message):
    await message.answer("🏡 Головна", reply_markup=kb.user_main_kb)
    User.get_or_create(id=message.from_user.id, username=message.from_user.username)


class NewSite(StatesGroup):
    link = State()
    period = State()


@user_router.message(F.text == "✍️ Зв'язок з адміністрацією")
async def new_site(message: Message):
    await message.answer(
        "Написати в",
        reply_markup=kb.ask_admin_inl,
    )


@user_router.message(F.text == "📜 Усі сайти")
async def new_site(message: Message):
    sites = Site.select().where(Site.user == message.from_user.id)
    msg = msgs.build_all_sites(sites)
    await message.answer(msg)


@user_router.message(F.text == "📝 Додати сайт")
async def new_site(message: Message, state: FSMContext):
    await message.answer(
        "Відправте посилання на сайт (`https://`)", reply_markup=kb.cancel_kb
    )
    await state.set_state(NewSite.link)


@user_router.message(NewSite.link)
async def new_link(message: Message, state: FSMContext):
    link = message.text
    if "https://" not in link:
        await message.reply(
            "🔴 Посилання не містить *http://*", reply_markup=kb.user_main_kb
        )
        await state.clear()
    elif link in [
        s.link for s in Site.select().where(Site.user == message.from_user.id)
    ]:
        await message.reply(
            "🔴 Ви вже додали данний сайт!", reply_markup=kb.user_main_kb
        )
        await state.clear()

    else:
        await message.answer(
            "Оберіть частоту перевірки", reply_markup=kb.get_period_kb()
        )
        await state.update_data(link=link)
        await state.set_state(NewSite.period)


# @user_router.message(NewSite.note)
# async def new_note(message: Message, state: FSMContext):
#     data = await state.get_data()
#     link = data.get("link")
#     await state.clear()
#     user = User.get_by_id(message.from_user.id)
#     site = Site(note=message.text, link=link, user=user)
#     site.save()
#     await message.answer("✅ Ви додали новий сайт!", reply_markup=kb.user_main_kb)


@user_router.message(NewSite.period)
async def new_note(message: Message, state: FSMContext):
    data = await state.get_data()
    link = data.get("link")
    await state.clear()
    user = User.get_by_id(message.from_user.id)
    period_seconds = periods[message.text]
    site = Site(check_period=period_seconds, link=link, user=user)
    site.save()
    await message.answer("✅ Ви додали новий сайт!", reply_markup=kb.user_main_kb)


@user_router.message(F.text == "test")
async def test(message: Message):
    await message.answer("bot works")
