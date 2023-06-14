import aiohttp
from loguru import logger
from app.models import Proxy, Site


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
