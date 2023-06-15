from pprint import pprint
import re
import aiohttp
from typing import NamedTuple, Sequence
from app.models import User, Site, Proxy, SiteStatus
import asyncio

from app.msgs import problem_with_site
from app.utils import send_warning


def _check_html_title(html_code):
    pattern = r"<title>(.*?)<\/title>"
    match = re.search(pattern, html_code)
    if match:
        return True
    else:
        return False


async def check_site(url: str, proxy: str) -> SiteStatus:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=proxy) as resp:
            if resp.status == 200:
                status_code = True
            else:
                return SiteStatus(status_code=False, html=False, ok=False, url=url)
            html = await resp.text()
            status_html = _check_html_title(html)
            ok = status_code and status_html
            return SiteStatus(status_code=status_code, html=status_html, ok=ok, url=url)


async def testing_sites(before_run_sec=100):
    await asyncio.sleep(before_run_sec)
    while True:
        proxy: Proxy = Proxy().select().first()

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
            print(f"Testing - {[s.link for s in sites]}\nSleep time - {sleep_sec}")
            for site in sites:
                status = await check_site(site.link, proxy.build_url())
                if not status.ok:
                    msg = problem_with_site(status)
                    # TODO send admin to (delete false below)
                    await send_warning(msg, site.user.id, False)
            await asyncio.sleep(sleep_sec)


async def test_time():
    c = 0
    while True:
        print(c)
        c += 1
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(testing())
