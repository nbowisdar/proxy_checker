# import argparse
# import asyncio
# from setup import dp, bot
# from app.models import Proxy
# from app.parsing import testing_sites

# parser = argparse.ArgumentParser()


# def _create_first_proxy():
#     parser.add_argument("-c", "--create_proxy", action="store_true")
#     args = parser.parse_args()

#     if args.create_proxy:
#         if Proxy.select().where(Proxy.name == "triolan"):
#             return
#         Proxy.create(
#             name="triolan",
#             address="185.112.12.134",
#             port=2831,
#             login="36547",
#             password="gyy5wFZD",
#         )


# async def _run_with_testing():
#     parser.add_argument("-np", "--notify_problems", action="store_true")
#     args = parser.parse_args()
#     if args.notify_problems:
#         async with asyncio.TaskGroup() as tg:
#             tg.create_task(testing_sites())
#             tg.create_task(dp.start_polling(bot))
#     else:
#         await dp.start_polling(bot)


# def run_with_flags():
#     _create_first_proxy()
#     _run_with_testing()
