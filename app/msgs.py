from app.models import Proxy, Site


def build_proxy_msg(p: Proxy) -> str:
    return f"{p.name.capitalize()}\n`{p.address}:{p.port}:{p.login}:{p.password}`"
