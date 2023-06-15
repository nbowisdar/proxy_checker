import datetime
from pprint import pprint
from typing import NamedTuple, Sequence
import peewee as pw
from enum import Enum

from app.structure.enums import Period

db = pw.SqliteDatabase("db.sqlite3")


class Proxy_Variant(Enum):
    TRIOLAN = "triolan"
    KYIVSTAR = "kyivstar"

    @classmethod
    def allowd_names(cls) -> list[str]:
        return [cls.KYIVSTAR.value, cls.TRIOLAN.value]

    @classmethod
    def is_allowed_proxy(cls, name) -> bool:
        if name in cls.allowd_names():
            return True
        return False


class BaseModel(pw.Model):
    class Meta:
        database = db


class User(BaseModel):
    # id = pw.IntegerField()
    username = pw.CharField(unique=True)


class Proxy(BaseModel):
    name = pw.CharField()
    address = pw.CharField()
    port = pw.IntegerField()
    login = pw.CharField()
    password = pw.CharField()

    @classmethod
    def get_proxy_status(cls) -> tuple[str, bool]:
        resp = []
        for proxy in Proxy_Variant.allowd_names():
            proxy_db = cls.select().where(cls.name == proxy).first()
            if proxy_db:
                status = True
            else:
                status = False
            resp.append((proxy, status))
        return resp

    def build_url(self) -> str:
        return f"http://{self.login}:{self.password}@{self.address}:{self.port}"


class Site(BaseModel):
    link = pw.CharField()
    # note = pw.CharField(null=True)
    check_period = pw.IntegerField()

    user = pw.ForeignKeyField(User, backref="sites")


# class DefaultOkFalse(BaseModel):
# ok = False
# real = False


class Status(BaseModel):
    status_code = pw.BooleanField()
    html = pw.BooleanField()
    ok = pw.BooleanField()
    # real = True
    # proxy: Proxy | None = None


class Error(BaseModel):
    user = pw.ForeignKeyField(User, backref="errors")
    link = pw.CharField()
    ok = pw.BooleanField()
    no_proxy = pw.ForeignKeyField(Status)
    triolan = pw.ForeignKeyField(Status, null=True)
    kyivstar = pw.ForeignKeyField(Status, null=True)

    created_at = pw.DateTimeField(default=datetime.datetime.now)


def create_tables():
    tables = [User, Proxy, Site, Status, Error]
    db.create_tables(tables)
