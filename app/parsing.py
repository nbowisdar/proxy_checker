from pprint import pprint
import re
from loguru import logger
import aiohttp
from typing import Sequence
from app.crud import save_error
from app.structure.models import (
    Proxy_Variant,
    Site,
    Proxy,
)

from app.structure.schemas import Status, Result, DefaultOkFalse

import asyncio

from app.msgs import build_warning_msg
from app.utils import send_warning


def _check_html_title(html_code):
    pattern = r"<title>(.*?)<\/title>"
    match = re.search(pattern, html_code)
    if match:
        return True
    else:
        return False


async def check_site(url: str, proxy: Proxy | None = None) -> Status:
    async with aiohttp.ClientSession() as session:
        proxy = None
        if proxy:
            # proxy_url = proxy.build_url()
            proxy = proxy.build_proxy_url()
        try:
            async with session.get(url, proxy=proxy) as resp:
                if resp.status == 200:
                    status_code = True
                else:
                    return Status(status_code=False, html=False)
                html = await resp.text()
                status_html = _check_html_title(html)
                ok = status_code and status_html
                return Status(status_code=status_code, html=status_html, ok=ok)
        except aiohttp.client_exceptions.ClientHttpProxyError:
            raise Exception(f"⚠️ Не можу приєднатися до проксі *{proxy.name}*")


async def _handle_results(bad_results: list[Result]):
    for bad_res in bad_results:
        # save result in db so to see it in statistics
        try:
            save_error(bad_res)
        except Exception as e:
            logger.error(e)
        msg = build_warning_msg(bad_res)
        logger.debug(f"try send message - {msg}")
        await send_warning(msg, user_id=bad_res.user_id, send_to_admin=False)


async def check_sites(sites: Sequence[Site]):
    results: list[Result] = []

    for site in sites:
        no_proxy = await check_site(site.link)

        triolan = DefaultOkFalse()
        kyivstar = DefaultOkFalse()

        for proxy in Proxy().select():
            if proxy.name == Proxy_Variant.TRIOLAN.value:
                triolan = await check_site(site.link, proxy)
            elif proxy.name == Proxy_Variant.KYIVSTAR.value:
                kyivstar = await check_site(site.link, proxy)

        ok = all([no_proxy.ok, triolan.ok, kyivstar.ok])
        results.append(
            Result(
                user_id=site.user.id,
                link=site.link,
                no_proxy=no_proxy,
                triolan=triolan,
                kyivstar=kyivstar,
                ok=ok,
            )
        )
    bad_results = list(filter(lambda r: not r.ok, results))
    if not bad_results:
        logger.debug("Everythins is okay")
        return True
    else:
        logger.debug(f"Bad results - {len(bad_results)}")
        await _handle_results(bad_results)


async def testing_sites(before_run_sec=100):
    await asyncio.sleep(before_run_sec)
    while True:
        for i in range(1, 4):
            # Select right sites
            match i:
                case 1:
                    sleep_sec = 600
                    sites: Sequence[Site] = Site.select().where(
                        Site.check_period == 600
                    )
                case 2:
                    sleep_sec = 1800
                    sites: Sequence[Site] = Site.select().where(
                        Site.check_period <= 1800
                    )
                case _:
                    sleep_sec = 3600

                    sites: Sequence[Site] = Site.select()
            await asyncio.sleep(sleep_sec)
            print(f"Testing - {[s.link for s in sites]}\nSleep time - {sleep_sec}")
            try:
                await check_sites(sites)

            except Exception as e:
                await send_warning(str(e), send_to_admin=True)


""" url: str
    ok: bool
    no_proxy: Status
    triolan: Status
    kyivstar: Status"""


async def test_time():
    c = 0
    while True:
        print(c)
        c += 1
        await asyncio.sleep(1)


# if __name__ == "__main__":
# asyncio.run(testing())
