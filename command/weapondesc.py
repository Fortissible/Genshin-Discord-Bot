from scrapper.web_scrapper import weapon_info_scrap
from utils.url_request import url_request

def weapon_desc(weap_name):
    weaps = weap_name.replace(' ', '_')
    page = f'https://genshin-impact.fandom.com/wiki/{weaps}'
    response = url_request(page)
    if response.status_code == 200:
        weapon = weapon_info_scrap(response)
        return weapon
    else:
        return None
