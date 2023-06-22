from setup import bot
import aiohttp
from loguru import logger
from app.structure.models import Proxy, Site
from config import admins_id


def get_status_symbol(b: bool) -> str:
    if b:
        return "🟢"
    return "🔴"


url = "https://www.google.com/"


async def _check_proxy(proxy: Proxy) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=proxy.build_url()) as response:
            if response.status != 200:
                raise Exception("Wrong status code")


async def check_proxy(proxy) -> bool:
    try:
        await _check_proxy(proxy)
        return True
    except Exception as err:
        logger.error(err)
        return False


async def send_warning(msg: str, *, user_id: int | None = None, send_to_admin=True):
    if user_id:
        await bot.send_message(user_id, msg)
    if send_to_admin:
        for a_id in admins_id:
            await bot.send_message(a_id, msg)
    logger.debug("Warning was sent")


def divide_big_msg(msg: str) -> list[str]:
    if len(msg) < 4000:
        return [msg]

    return msg.split("\n\n")


# def
