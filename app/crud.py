from typing import Sequence
from app.structure.enums import Period
from app.structure.models import Site, Proxy, Error


def get_proxy_by_name(name: str) -> Proxy | None:
    proxy = Proxy.select().where(Proxy.name == name).first()
    return proxy


def get_errs_by_period(period: Period) -> Sequence[Error]:
    return Error.select().where(period.value < Error.created_at)
