from app.models import Proxy, Site, SiteStatus
from app.utils import get_status_symbol


def build_proxy_msg(p: Proxy) -> str:
    return f"{p.name.capitalize()}\n`{p.address}:{p.port}:{p.login}:{p.password}`"


def build_all_sites(sites: list[Site]) -> str:
    if not sites:
        return "⚠️ Ви ще не додали жодного посилання!"
    data = []
    for site in sites:
        per = site.check_period // 60
        data.append(f"Сайт - {site.link}\nПеріод перевірки - {per} мін.\n")
    return "\n".join(data)


def problem_with_site(site: SiteStatus) -> str:
    return f"""
⚠️ Site - {site.url}
status code {get_status_symbol(site.status_code)}
html {get_status_symbol(site.html)}
"""
