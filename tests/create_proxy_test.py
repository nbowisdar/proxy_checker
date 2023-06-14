import argparse

from app.models import Proxy


def create_first_proxy():
    parser = argparse.ArgumentParser(description="Description of your script")
    parser.add_argument("-c", "--create_proxy", action="store_true")
    args = parser.parse_args()

    if args.create_proxy:
        if Proxy.select().where(Proxy.name == "triolan"):
            return
        Proxy.create(
            name="triolan",
            address="185.112.12.134",
            port=2831,
            login="36547",
            password="gyy5wFZD",
        )
