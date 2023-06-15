from datetime import datetime, timedelta
from enum import Enum


# class Proxy_Variant(Enum):
#     TRIOLAN = "triolan"
#     KYIVSTAR = "kyivstar"


class Period(Enum):
    day = datetime.now() - timedelta(days=1)
    week = datetime.now() - timedelta(days=7)
    month = datetime.now() - timedelta(days=30)
    three_months = datetime.now() - timedelta(days=90)
    year = datetime.now() - timedelta(days=360)
    all_time = datetime(year=2000, month=1, day=1)
