import requests
from bs4 import BeautifulSoup
from data.class_data import character
from data.strings_data import data

if __name__ == "__main__":
    char_query = input("input nama karakter\n")
    char = character()
    char_name = ""
    if char_query in data().char_dict:
        char_name = data().char_dict[char_query.capitalize()]
    else:
        char_name = char_query
    page = f'https://genshin-impact.fandom.com/wiki/{char_name}'
    response = requests.get(page)
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
