from web_scrapper import event_news_scrap
from utils import url_request

def event_news(type=0):
    page = f'https://genshin-impact.fandom.com/wiki/Event'
    response = url_request(page)
    if response.status_code == 200:
        titles, imgs, durations, event_type = event_news_scrap(type,response)
        return titles, imgs, durations, event_type
    else:
        return [], [], [], []
