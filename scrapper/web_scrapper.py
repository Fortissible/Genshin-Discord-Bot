from bs4 import BeautifulSoup
from data.class_data import *


def event_news_scrap(type, response):
    soup = BeautifulSoup(response.text, 'html.parser')
    table_list = soup.findAll("table", {"class": "wikitable sortable"})
    titles = []
    imgs = []
    durations = []
    event_type = []
    for rows in table_list[type].findAll("tr"):
        for row in rows:
            # for a_title in row.findAll("a"):
            #     if (str(a_title.text) != ""):
            #         titles.append(a_title.text)
            for a_imgs in row.findAll("img"):
                http_link = "https://"
                for img_link in a_imgs.attrs.values():
                    if http_link in img_link:
                        imgs.append(img_link)
        counter = 0
        for tds in rows.find_all("td"):
            counter += 1
            if counter % 3 == 1:
                titles.append(tds.text)
            elif counter % 3 == 2:
                durations.append(tds.text)
            else:
                event_type.append(tds.text)
    return titles, imgs, durations, event_type


def weapon_info_scrap(response):
    weapon_info = weapon()

    soup = BeautifulSoup(response.text, 'html.parser')
    weapon_info_card = soup.findAll('aside')[0]

    weapon_info.weapon_name = weapon_info_card.find('h2', {'data-source': 'title'}).text
    weapon_info.weapon_type = weapon_info_card.findAll('section')[0].findAll('div')[2].find('a')['title']
    weapon_info.weapon_rarity = weapon_info_card.findAll('section')[0].findAll('div')[2].findAll('div')[2].find('img')[
        'title']
    weapon_info.weapon_base_atk = weapon_info_card.findAll('section')[2].findAll('div')[0].text
    weapon_info.weapon_stat_type = weapon_info_card.findAll('section')[2].findAll('div')[1].text
    weapon_info.weapon_stat_base = weapon_info_card.findAll('section')[2].findAll('div')[2].text
    weapon_info.weapon_desc_title = weapon_info_card.findAll('section')[9].find('th').text
    weapon_info.weapon_desc = weapon_info_card.findAll('section')[9].find('td').text
    weapon_info.weapon_img_link = weapon_info_card.findAll('div')[0].find('a')['href']

    return weapon_info


def youtube_video_scrap(response):
    list_link = []
    soup = BeautifulSoup(response.text, 'html.parser')
    str_soup = str(soup)
    parser = str_soup.find("https://www.youtube.com/watch")

    counter = 0
    format = 47

    link = ""
    link += str_soup[parser:parser + 47]
    link = link.replace("%3Fv%3D", "?v=")
    list_link.append(link)

    while counter < 15 and str_soup[parser + format + 1:].find("https://www.youtube.com/watch") + parser != -1:
        link = ""
        parser = str_soup[parser + format + 1:].find("https://www.youtube.com/watch") + parser
        link += str_soup[parser + format + 1:parser + format + 1 + 47]
        link = link.replace("%3Fv%3D", "?v=")
        list_link.append(link)
        format += 47
        counter += 1

    return list_link
