from pprint import pprint
import peewee as pw
from enum import Enum


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

    @classmethod
    def get_fields(cls):
        fields = cls._meta.fields
        pprint(fields)


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
        # "http://36547:gyy5wFZD@185.112.12.134:2831"
        return f"http://{self.login}:{self.password}@{self.address}:{self.port}"


class Site(BaseModel):
    name = pw.CharField(null=True)
    link = pw.CharField(unique=True)


def create_tables():
    tables = [Proxy, Site]
    db.create_tables(tables)
