import requests
from bs4 import BeautifulSoup
from data.class_data import weapon

if __name__=="__main__":
    page = f'https://genshin-impact.fandom.com/wiki/Mailed_Flower'
    response = requests.get(page)
    if response.status_code == 200:
        weapon_info = weapon()

        soup = BeautifulSoup(response.text, 'html.parser')
        weapon_info_card = soup.findAll('aside')[0]

        weapon_info.weapon_name = weapon_info_card.find('h2',{'data-source':'title'}).text
        weapon_info.weapon_type = weapon_info_card.findAll('section')[0].findAll('div')[2].find('a')['title']
        weapon_info.weapon_rarity = weapon_info_card.findAll('section')[0].findAll('div')[2].findAll('div')[2].find('img')['title']
        weapon_info.weapon_base_atk = weapon_info_card.findAll('section')[2].findAll('div')[0].text
        weapon_info.weapon_stat_type = weapon_info_card.findAll('section')[2].findAll('div')[1].text
        weapon_info.weapon_stat_base = weapon_info_card.findAll('section')[2].findAll('div')[2].text
        weapon_info.weapon_desc_title = weapon_info_card.findAll('section')[9].find('th').text
        weapon_info.weapon_desc = weapon_info_card.findAll('section')[9].find('td').text
        weapon_info.weapon_img_link = weapon_info_card.findAll('div')[0].find('a')['href']
