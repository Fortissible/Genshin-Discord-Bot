from scrapper.web_scrapper import char_information_scrap
from utils.url_request import url_request
from data.strings_data import data


def char_info(char_query):
    if char_query in data().char_dict:
        char_name = data().char_dict[char_query.capitalize()]
    else:
        char_name = char_query
    page = f'https://genshin-impact.fandom.com/wiki/{char_name}'
    response = url_request(page)
    if response.status_code == 200:
        char = char_information_scrap(response)
        return char
    else:
        return None
