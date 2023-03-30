import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from data.class_data import character
from data.strings_data import data
from tabulate import tabulate

if __name__ == "__main__":
    page = f'https://genshin-impact.fandom.com/wiki/Character'
    response = requests.get(page)
    soup = BeautifulSoup(response.text, 'html.parser')
    char_list_info = []

    for i in range(0,len(soup.findAll('table')[1].findAll('td')),7):
        if soup.findAll('table')[1].findAll('td')[i+1].find('a').text == "Traveler" :
            char_list_info.append([soup.findAll('table')[1].findAll('td')[i + 1].find('a').text,
                                   soup.findAll('table')[1].findAll('td')[i + 2].find('img')['title'],
                                   "None",
                                   soup.findAll('table')[1].findAll('td')[i + 4].find('a')['title'],
                                   "OuterSpace"])
        elif soup.findAll('table')[1].findAll('td')[i+1].find('a').text == "Aloy" :
            char_list_info.append([soup.findAll('table')[1].findAll('td')[i + 1].find('a').text,
                                   soup.findAll('table')[1].findAll('td')[i + 2].find('img')['title'],
                                   soup.findAll('table')[1].findAll('td')[i + 3].find('a')['title'],
                                   soup.findAll('table')[1].findAll('td')[i + 4].find('a')['title'],
                                   "HorizonZeroDawn"])
        else :
            char_list_info.append([soup.findAll('table')[1].findAll('td')[i + 1].find('a').text,
                                   soup.findAll('table')[1].findAll('td')[i + 2].find('img')['title'],
                                   soup.findAll('table')[1].findAll('td')[i + 3].find('a')['title'],
                                   soup.findAll('table')[1].findAll('td')[i + 4].find('a')['title'],
                                   soup.findAll('table')[1].findAll('td')[i+5].find('a')['title']])
    char_df = pd.DataFrame(np.array(char_list_info), columns=['Name', 'Rarity', 'Element', 'Weapon', 'Region'])
    chars_table = tabulate(char_df,headers='keys',tablefmt='psql')
    print(chars_table)

    # table_rows = soup.find('div',{'class':'talent-table-container'}).findAll('tr')
    # for idx,val in enumerate(table_rows):
    #     if val.find('a',{'title':'Elemental Skill'}):
    #         print(idx)
    #     print(f"pada index ke-{idx}","\n",val,"\n")

    # char_talent_title = [ table_rows[i+1] for i in range(len(table_rows)-1) if (i+1)%2==1]
    # char_talent_detail = [ table_rows[i+1] for i in range(len(table_rows)-1) if (i+1)%2==0]

    # for i in soup.find("tbody").findAll('a'):
    #     if len(i.text) != 0 :
    #         print(i.text)
    #     else :
    #         print("kosong gan")

    # endpoint = soup.find("tbody").find('a')['href']
    # chartalent_info = f"{base_link}{endpoint}"
    # print(chartalent_info)

    # strings = data.abbrevation()
    # i = 0
    # type = data.char_skills
    # page = f"https://genshin.honeyhunterworld.com/db/char/{char}"
    # response = requests.get(page)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # headers = []
    # datass = []
    # if response.status_code == 200:
    #     tables = soup.find_all("table", {'class': 'add_stat_table'})
    #     tables.remove(tables[0])
    #     tables.remove(tables[0])
    #     if (char == "ayaka" or char == "mona"):
    #         tables.remove(tables[2])
    #     a = 3
    #     b = 0
    #     while (a > 0):
    #         tab = tables[b].find_all('tr')
    #         b += 1
    #         a -= 1
    #         c = 0
    #         header = []
    #         datas = []
    #         for tr in tab:
    #             data = []
    #             tds = tr.find_all('td')
    #             d = 0
    #             for td in tds:
    #                 temp = ""
    #                 if c == 0 and d <= 13:
    #                     header.append(td.text)
    #                 elif d <= 13:
    #                     temp = td.text
    #                     for string in strings:
    #                         temp = temp.replace(string, strings[string])
    #                     temp = temp.replace(":", "")
    #                     temp = temp.replace(" ", "\n")
    #                     temp = temp.replace("-", "\n-\n")
    #                     temp = temp.replace("/", "\n/\n")
    #                     temp = temp.replace("×", "\n×\n")
    #                     if d == 0:
    #                         temp = "+" + temp
    #                     data.append(temp)
    #                 else:
    #                     break
    #                 d += 1
    #             if c == 0:
    #                 headers.append(header)
    #             else:
    #                 datas.append(data)
    #             c += 1
    #         datass.append(datas)
    # for header, datas in zip(headers, datass):
    #     i += 1
    #     header.remove(header[3])
    #     header.remove(header[4])
    #     header.remove(header[5])
    #     header.remove(header[9])
    #     header.remove(header[6])
    #     header.remove(header[7])
    #     for data in datas:
    #         data.remove(data[3])
    #         data.remove(data[4])
    #         data.remove(data[5])
    #         data.remove(data[9])
    #         data.remove(data[6])
    #         data.remove(data[7])
    #     x = (tabulate(datas, header))
