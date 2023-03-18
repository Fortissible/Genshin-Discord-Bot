import os,discord,json,random,requests,urllib.request
import re
from bs4 import BeautifulSoup
from discord.ext import commands
from tabulate import tabulate

if __name__=="__main__":
    page = f'https://genshin-impact.fandom.com/wiki/Event'
    response = requests.get(page)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table_list = soup.findAll("table",{"class":"wikitable sortable"})
        titles = []
        imgs = []
        durations = []
        event_type =[]
        for rows in table_list[1].findAll("tr"):
            for row in rows:
                for a_imgs in row.findAll("img"):
                    http_link = "https://"
                    for img_link in a_imgs.attrs.values():
                        if http_link in img_link :
                            imgs.append(img_link)
            counter = 0
            for tds in rows.find_all("td"):
                counter += 1
                if counter%3 == 1:
                    titles.append(tds.text)
                elif counter%3 == 2 :
                    durations.append(tds.text)
                else :
                    event_type.append(tds.text)
            counter = 0