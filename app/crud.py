from pprint import pprint
from typing import Sequence
from app.structure.enums import Period
from app.structure.models import Site, Proxy, Error, Status, db
from app.structure import schemas


def get_proxy_by_name(name: str) -> Proxy | None:
    proxy = Proxy.select().where(Proxy.name == name).first()
    return proxy


def get_errs_by_period(period: Period) -> Sequence[Error]:
    return Error.select().where(period.value < Error.created_at)


"""
    user = pw.ForeignKeyField(User, backref="errors")
    link = pw.CharField()
    ok = pw.BooleanField()
    no_proxy = pw.ForeignKeyField(Status)
    triolan = pw.ForeignKeyField(Status, null=True)
    kyivstar = pw.ForeignKeyField(Status, null=True)
    """


def _save_status(status: schemas.Status) -> Status:
    if status.real:
        return Status.create(**status.dict())


def save_error(r: schemas.Result):
    pprint(r.no_proxy.dict())
    pprint(r.triolan.dict())
    pprint(r.kyivstar.dict())
    with db.atomic():
        no_proxy = _save_status(r.no_proxy)
        triolan = _save_status(r.triolan)
        kyivstar = _save_status(r.kyivstar)
        Error.create(
            user=r.user_id,
            link=r.link,
            no_proxy=no_proxy,
            triolan=triolan,
            kyivstar=kyivstar,
        )


# def from_error_to_result(errors: Sequence[Error]) -> list[schemas.Result]:
