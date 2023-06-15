from app.main import run_with_flags
from setup import bot, dp
from app.models import create_tables
from app.handlers.admin_handlers import admin_router
from app.handlers.user_handlers import user_router
import asyncio
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)
from loguru import logger
from app.middleware.admin_only import AdminOnly


async def _start():
    admin_router.message.middleware(AdminOnly())
    dp.include_router(admin_router)
    dp.include_router(user_router)

    await run_with_flags()


def start_simple():
    asyncio.run(_start())


# async def on_startup(bot: Bot, base_url: str):
#     await bot.set_webhook(f"{base_url}")


# async def on_shutdown(bot: Bot, base_url: str):
#     await bot.delete_webhook()


# def start_webhook():
#     # dp["base_url"] = ngrok_url
#     dp.startup.register(on_startup)
#     dp.shutdown.register(on_shutdown)
#     dp.include_router(admin_router)

#     app = web.Application()
#     app["bot"] = bot
#     SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="")
#     setup_application(app, dp, bot=bot)
#     web.run_app(app, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    try:
        create_tables()
        start_simple()  # run without webhook
        # start_webhook()  # run tg bot
    except KeyboardInterrupt:
        logger.info("Bot stopped by admin")
