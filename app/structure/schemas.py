from typing import NamedTuple
from pydantic import BaseModel
from app.structure.enums import Period


per_by_name = {
    "week": Period.week,
    "day": Period.day,
    "month": Period.month,
    "3months": Period.three_months,
    "year": Period.year,
    "all_time": Period.all_time,
}


class DefaultOkFalse(BaseModel):
    ok = False
    real = False


class Status(BaseModel):
    status_code: bool
    html: bool
    ok: bool
    real = True
    # proxy: Proxy | None = None


class Result(BaseModel):
    user_id: int
    link: str
    ok: bool
    no_proxy: Status
    triolan: Status | DefaultOkFalse
    kyivstar: Status | DefaultOkFalse
