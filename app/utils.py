import aiogram
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
        async with session.get(url, proxy=proxy.build_proxy_url()) as response:
            if response.status != 200:
                raise Exception("Wrong status code")


async def check_proxy(proxy: Proxy) -> bool:
    try:
        await _check_proxy(proxy)
        return True
    except Exception as err:
        logger.error(err)
        return False


async def send_warning(msg: str, *, user_id: int | None = None, send_to_admin=True):
    if user_id:
        try:
            await bot.send_message(user_id, msg)
        except aiogram.exceptions.TelegramForbiddenError:
            pass
    if send_to_admin:
        for a_id in admins_id:
            try:
                await bot.send_message(a_id, msg)
            except aiogram.exceptions.TelegramForbiddenError:
                logger.error(f"Admin blocks bot {a_id}")
    logger.debug("Warning was sent")


# def divide_big_msg(msg: str) -> list[str]:
def divide_big_msg(text, max_length=4096) -> list[str]:
    """
    Divides a long message into smaller chunks suitable for Telegram.

    Args:
        text (str): The long message to be divided.
        max_length (int): Maximum length of each chunk (default: 4096).

    Returns:
        list: A list of message chunks.
    """
    chunks = []
    if len(text) <= max_length:
        # If the message is already within the maximum length, return it as is
        chunks.append(text)
    else:
        # Divide the message into chunks of maximum length
        while len(text) > 0:
            if len(text) <= max_length:
                chunks.append(text)
                break
            chunk = text[:max_length]
            last_space = chunk.rfind(" ")
            if last_space != -1:
                chunk = chunk[:last_space]
            chunks.append(chunk)
            text = text[len(chunk) :].lstrip()
    return chunks


# def
