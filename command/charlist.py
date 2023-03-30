from scrapper.web_scrapper import characters_scrap
from utils.url_request import url_request


def character_list(elm):
    page = f'https://genshin-impact.fandom.com/wiki/Character'
    response = url_request(page)
    if response.status_code == 200:
        chars = characters_scrap(response, elm)
        return chars
    else:
        return None
