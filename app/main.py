from argparse import ArgumentParser
import asyncio
from setup import dp, bot
from app.structure.models import Proxy
from app.parsing import testing_sites
from loguru import logger


parser = ArgumentParser()


def _pars_args() -> ArgumentParser:
    parser.add_argument("-c", "--create_proxy", action="store_true")
    parser.add_argument("-np", "--notify_problems", action="store_true")
    return parser.parse_args()


def _create_first_proxy(args: ArgumentParser):
    if args.create_proxy:
        logger.info("Test proxy created")
        if Proxy.select().where(Proxy.name == "triolan"):
            return
        Proxy.create(
            name="triolan",
            address="185.112.12.134",
            port=2831,
            login="36547",
            password="gyy5wFZD",
        )


async def _run_with_testing(args: ArgumentParser):
    if args.notify_problems:
        logger.info("Run bot with notification")

        async with asyncio.TaskGroup() as tg:
            tg.create_task(testing_sites(1))
            tg.create_task(dp.start_polling(bot))

    else:
        logger.info("Run bot only")
        await dp.start_polling(bot)


async def run_with_flags():
    args = _pars_args()
    _create_first_proxy(args)
    await _run_with_testing(args)
