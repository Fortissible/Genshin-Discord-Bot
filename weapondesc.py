from utils import url_request
from web_scrapper import weapon_info_scrap


def weapon_desc(weap_name):
    weaps = weap_name.replace(' ', '_')
    page = f'https://genshin-impact.fandom.com/wiki/{weaps}'
    response = url_request(page)
    if response.status_code == 200:
        weapon = weapon_info_scrap(response)
        return weapon
    else:
        return None
