from bs4 import BeautifulSoup
from data.class_data import *
from data.strings_data import *
import numpy as np
import pandas as pd
from tabulate import tabulate


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


def char_information_scrap(response):
    char = character()

    soup = BeautifulSoup(response.text, 'html.parser')
    card_data = soup.findAll('aside')[0]

    char.char_name = card_data.findAll('h2')[0].text
    char.char_title = card_data.findAll('h2')[1].text
    char.char_img = card_data.find('a')["href"]
    char_type_section = card_data.findAll('section')[0].findAll('td')
    char_desc_section = card_data.findAll('section')[1].findAll('div')
    char.char_rarity = char_type_section[0].find('img')['title']
    char.char_weap = char_type_section[1].text
    char.char_element = char_type_section[2].text
    char.char_nation = char_desc_section[11].text
    char.char_sex = char_desc_section[6].text
    char.char_bday = char_desc_section[7].text
    char.char_affiliation = ""
    for i in range(0, len(char_desc_section[13].findAll('a')) - 1):
        char.char_affiliation += char_desc_section[13].findAll('a')[i].text + "; "

    return char


def characters_scrap(response, elm):
    soup = BeautifulSoup(response.text, 'html.parser')
    char_list_info = []

    for i in range(0, len(soup.findAll('table')[1].findAll('td')), 7):
        if soup.findAll('table')[1].findAll('td')[i + 1].find('a').text == "Traveler":
            char_list_info.append([soup.findAll('table')[1].findAll('td')[i + 1].find('a').text,
                                   soup.findAll('table')[1].findAll('td')[i + 2].find('img')['title'],
                                   "None",
                                   soup.findAll('table')[1].findAll('td')[i + 4].find('a')['title'],
                                   "OuterSpace"])
        elif soup.findAll('table')[1].findAll('td')[i + 1].find('a').text == "Aloy":
            char_list_info.append([soup.findAll('table')[1].findAll('td')[i + 1].find('a').text,
                                   soup.findAll('table')[1].findAll('td')[i + 2].find('img')['title'],
                                   soup.findAll('table')[1].findAll('td')[i + 3].find('a')['title'],
                                   soup.findAll('table')[1].findAll('td')[i + 4].find('a')['title'],
                                   "HorizonZeroDawn"])
        else:
            char_list_info.append([soup.findAll('table')[1].findAll('td')[i + 1].find('a').text,
                                   soup.findAll('table')[1].findAll('td')[i + 2].find('img')['title'],
                                   soup.findAll('table')[1].findAll('td')[i + 3].find('a')['title'],
                                   soup.findAll('table')[1].findAll('td')[i + 4].find('a')['title'],
                                   soup.findAll('table')[1].findAll('td')[i + 5].find('a')['title']])
    char_df = pd.DataFrame(np.array(char_list_info), columns=['Name', 'Rarity', 'Element', 'Weapon', 'Region'])
    chars_table = tabulate(char_df, headers='keys', tablefmt='psql')
    return chars_table
