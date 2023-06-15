from app.structure.models import Proxy, Site, Error
from app.utils import get_status_symbol
from app.structure.schemas import Status, Result
from typing import Sequence
from datetime import datetime, date


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


def build_error_statistic(errors: Sequence[Error]) -> str:
    # TODO build the right messages here
    # base = f"⚠️ - {len(errors)}"
    base = f""

    units = []
    cur_date = None
    # cur_date = datetime.now().date()
    for e in errors:
        other_date = ""
        if e.created_at.date() != cur_date:
            other_date = f"Дата - {e.created_at.date()}\n"
            cur_date = e.created_at.date()
        if e.no_proxy:
            code_s = get_status_symbol(e.no_proxy.status_code)
            html_s = get_status_symbol(e.no_proxy.html)
        else:
            code_s = "⚠️"
            html_s = "⚠️"
        if e.triolan:
            code_t = get_status_symbol(e.triolan.status_code)
            html_t = get_status_symbol(e.triolan.html)
        else:
            code_t = "⚠️"
            html_t = "⚠️"
        if e.kyivstar:
            code_k = get_status_symbol(e.kyivstar.status_code)
            html_k = get_status_symbol(e.kyivstar.html)
        else:
            code_k = "⚠️"
            html_k = "⚠️"
        units.append(
            f"""
{other_date}{e.link}
код от. (S. {code_s}, T {code_t}, K {code_k}) | html (S. {html_s}, T {html_t}, K {html_k}) 
            """
        )
    return base + "".join(units)
