from app.models import Site, Proxy


def get_proxy_by_name(name: str) -> Proxy | None:
    proxy = Proxy.select().where(Proxy.name == name).first()
    return proxy
    # if proxy:
    #     return proxy
    # raise Exception(f"Proxy with name {name} doesn't exist")
