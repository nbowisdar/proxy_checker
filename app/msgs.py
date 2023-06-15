from app.models import Proxy, Site, Status, Result
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


def build_warning_msg(br: Result) -> str:
    "site.com | код от. (S. 🟢, T 🔴, K 🟢) | html (S. 🟢, T 🔴, K 🟢)"

    default = "❕ Вимкненно"
    triolan, kyivstar = default, default

    if br.triolan.real:
        triolan = f"""
{get_status_symbol(br.triolan.status_code)} Code | {get_status_symbol(br.triolan.html)} HTML
        """
    if br.kyivstar.real:
        kyivstar = f"""
{get_status_symbol(br.kyivstar.status_code)} Code | {get_status_symbol(br.kyivstar.html)} HTML
        """

    return f"""
⚠️   {br.link}

No proxy:
{get_status_symbol(br.no_proxy.status_code)} Code | {get_status_symbol(br.no_proxy.html)} HTML

Triolan: {triolan}
Kyivstar: {kyivstar}

"""
