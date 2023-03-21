from scrapper.web_scrapper import youtube_video_scrap
from utils.url_request import url_request

def youtube_video(search):
    page = f'https://www.google.com/search?q=youtube+{search}'
    response = url_request(page)
    if response.status_code == 200:
        list_link = youtube_video_scrap(response)
        return list_link
    else:
        return None