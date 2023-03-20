from bs4 import BeautifulSoup
from classdata import *


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
    soup = BeautifulSoup(response.text, 'html.parser')
    weapon_info = weapon()
    a = soup.find('aside')

    fg = a.find('figure')
    img = fg.find('a', {'class': 'image image-thumbnail'})
    gmbr = img.find('img')
    img_link = gmbr['src']
    print(img_link)
    weapon_info.weapon_name = weap

    div1 = a.find('div', {'data-source': 'type'})
    type = div1.find('a')
    print(type.text)
    weapon_info.weapon_type = type.text

    div2 = a.find('div', {'data-source': 'rarity'})
    rar = div2.find('img')
    rarity = rar['title']
    print(rarity)
    weapon_info.weapon_rarity = rarity

    div3 = a.find('section', {'class': 'pi-item pi-group pi-border-color'})
    st = div3.find('table')
    tab = st.find('tbody')
    stat = tab.find_all('td')
    print(stat[0].text)
    print(stat[1].text)
    print(stat[2].text)
    weapon_info.weapon_base_atk = stat[0].text
    weapon_info.weapon_stat_type = stat[1].text
    weapon_info.weapon_stat_base = stat[2].text

    div4 = a.find('section', {'class': 'pi-item pi-panel pi-border-color wds-tabber'})
    desk = div4.find('table')

    head = desk.find('thead')
    th = head.find('th')

    weapon_info.weapon_desc_title = th.text

    body = desk.find('tbody')
    td = body.find('td')
    print(td.text)

    weapon_info.weapon_desc = td.text

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

    while (counter < 15 and str_soup[parser + format + 1:].find("https://www.youtube.com/watch") + parser != -1):
        link = ""
        parser = str_soup[parser + format + 1:].find("https://www.youtube.com/watch") + parser
        link += str_soup[parser + format + 1:parser + format + 1 + 47]
        link = link.replace("%3Fv%3D", "?v=")
        list_link.append(link)
        format += 47
        counter += 1

    return list_link
