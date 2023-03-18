import os,discord,json,random,requests,urllib.request
from bs4 import BeautifulSoup
from discord.ext import commands
from tabulate import tabulate
from eventnews import event_news

#tkn = os.environ['tok']
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents)

notes = "\n**Command prefix [~]**" \
        "\n\n**List Command**\n\n" \
        "~ping      : ngecek ping" \
        "```yaml\n" \
        "contoh : ~ping```" \
        "~calcdmg   : [attack][critdmg%][talentattack%][elebonus%]" \
        "```yaml\n" \
        "contoh : ~calcdmg 2109 150.7 704.2 45.6```" \
        "~calcresin : [timestart][timeend]" \
        "```yaml\n" \
        "contoh : ~calcresin 17.44 22.20```" \
        "~pics       : [chara][*(series)][/tags]" \
        "```yaml\n" \
        "contoh : ~pics ganyu (genshin impact)\n" \
        "contoh : ~pics ganyu (genshin impact)/office\n" \
        "contoh : ~pics mona (genshin impact)/swimsuit\n" \
        "contoh : ~pics hatsune miku/swimsuit\n" \
        "* optional```" \
        "~calcprim   : [Jumlah Hari] [Banyak event/bulan] [Durasi Blessing(hari)] " \
        "```yaml\n" \
        "contoh : ~calcprim 60 15 1```" \
        "~maps : Map untuk Farm apapun" \
        "```yaml\n" \
        "contoh : ~maps```" \
        "~charlist   : [element atau all]" \
        "```yaml\n" \
        "contoh : ~charlist anemo    ~charlist all```"\
        "~talent : [char]"\
        "```yaml\n"\
        "contoh : ~talent ayaka```"\
        "~info  : [Nama Character] (Jika lebih dari 1 kata gunakan Underline'_') " \
        "```yaml\n" \
        "contoh : ~info Hu_Tao```" \
        "~nonton : [Nama Video] " \
        "```yaml\n" \
        "contoh : ~nonton Ganyu wangi```"\
        "~wp : [Nama Weapon] (Jika lebih dari 1 kata gunakan Underline'_')" \
        "```yaml\n" \
        "contoh : ~wp Skyward_Harp```"

bot.remove_command('help')

def get_gelImage(tags):
    """Returns pictures from Gelbooru with given tags."""
    tags = list(tags)
    formatted_tags = ""
    rating = ""

    ratings = {
        "re": "rating%3aexplicit",
        "rq": "rating%3aquestionable",
        "rs": "rating%3asafe"
    }

    if tags:  # if there are any tags, check for ratings
        if tags[0] in ratings:
            rating = ratings[tags[0]]
            tags.remove(tags[0])

    if rating == "":  # if rating wasn't specified, set safe one
        rating = ratings["rs"]

    if ((tags[len(tags)-1]).isdigit()):
        halaman = tags[len(tags)-1]
        tags.remove(tags[len(tags)-1])
    else :
        halaman = '1'

    # make tags suitable for Gelbooru API url
    formatted_tags = "_".join(tags).replace("/","+")

    print(rating, formatted_tags)

    '''
    api_url = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=50&tags={rating}+{formatted_tags}"
    '''

    api_url = f"https://danbooru.donmai.us/posts.json?page={halaman}&tags={rating}+{formatted_tags}"

    response = requests.get(api_url)

    # parsing json
    json_api_url = json.loads(response.text)

    # verify if there is anything within given tags
    if json_api_url:
        image = random.choice(json_api_url)["file_url"]
        return image
    else:
        return "Tidak ada hasil terkait, mungkin terjadi kesalahan pada nama karakter atau seri asalnya."


@bot.event
async def on_ready():
  print('{0.user} ready to go for new Adventure!'.format(bot))

@bot.command()
async def ping(ctx):
  await ctx.send(f'Bacot! [{round(bot.latency *1000)}ms]')

@bot.command()
async def helps(ctx):
  await ctx.send(notes)

@bot.command()
async def calcdmg(ctx, att, cd, ability, elebonus):
    res = int(att) * (float(ability) / 100) * (float(elebonus) / 100)* (1 + float(cd) / 100)
    bsra = " Besar Attack = " + str(int(att))
    crd  = " Besar Critical damage = " + str(cd) + "%"
    elmb = " Besar Elemental Bonus = " + str(elebonus) + "%"
    talt = " Talent Damage = " + str(ability) + "%"
    a = " Total Damage yang diperoleh = " + str(int(res))
    output = "```yaml\n+{}\n+{}\n+{}\n+{}\n+{}```".format(bsra,crd,elmb,talt,a)
    await ctx.send(output)

@bot.command()
async def calcresin(ctx,a,b):
  timestart = float(a)
  wktm = "Waktu Mulai : " + str(timestart)
  timeend = float(b)
  wkta = "Waktu Akhir : " + str(timeend)
  menit1 = abs((int(timeend)-int(timestart))*60)
  menit2 = ((timeend%1)-(timestart%1))*100
  res = int((menit1+menit2)/8)
  total = "Resin yang didapat : " + str(res)

  await ctx.send("```yaml\n+{}\n+{}\n+{}```".format(wktm,wkta,total))

@bot.command()
async def calcprim(ctx, hr, evnt, blessing):
  abs_init = 600
  if (int(blessing)>int(hr)):
      blessing = hr
  res   = ( 60*int(hr) ) + ( 90*int(blessing) )
  daily = " Daily = " + hr + " x " + str(60) + " = " + str( 60*int(hr) ) + "\n"
  event = " Event bulanan = " + evnt + " x " + str(420) + " = "  + str(int(evnt)*420) + "\n"
  abs   = " Abyss Floor = " + str( abs_init + (int(int(hr)/14)*600) ) + "\n"
  blss  = " Blessing = "  + blessing + " x " + str(90) + " = " + str( 90 * int(blessing) ) + "\n"
  mix   = " Total primogem = " + str( res + abs_init + (int(int(hr)/14)*600) + int(evnt)*420)
  output = "```yaml\n+{}+{}+{}+{}+{}```".format(daily,event,abs,blss,mix)
  await ctx.send(output)

# ---------------- img bot ------------------
@bot.command()
async def pics(ctx, *tags):
    """Calls get_gelImage() with tags specified by user, then sends an image."""
    if "rq" in tags or "re" in tags:
        if ctx.channel.is_nsfw():  # check if channel is suitable for given rating
            img = get_gelImage(tags)
            return await ctx.send(img)
        else:
            message = "For rating questionable or explicit NSFW channel is required!"
            return await ctx.send(message)
    img = get_gelImage(tags)
    await ctx.send(img)

@bot.command()
async def maps(ctx):
  await ctx.send("```yaml\n\t\t\t\t-------- Map Farm Genshin Impact --------\n\ncopy link : https://webstatic-sea.mihoyo.com/app/ys-map-sea/?lang=id-id#```")

@bot.command()
async def charlist(ctx,elm):
    if elm == "pyro" :
        await ctx.send("```yaml\n\t\t-------- Pyro Character Genshin --------\n\n+ Amber ★★★★\n+ Bennet ★★★★ \n+ Xiangling ★★★★\n+ Xinyann ★★★★\n+ yanfei ★★★★\n+ Diluc ★★★★★\n+ Klee ★★★★★\n+ Hu Tao ★★★★★\n+ Yoimiya ★★★★★```")
    elif elm == "anemo" :
        await ctx.send("```yaml\n\t\t-------- anemo Character Genshin --------\n\n+ Sucrose ★★★★\n+ Sayu ★★★★ \n+ Jean ★★★★★\n+ venti ★★★★★\n+ Xiao ★★★★★\n+ Kaedehara Kazuha ★★★★★```")
    elif elm == "cryo" :
        await ctx.send("```yaml\n\t\t-------- Cryo Character Genshin --------\n\n+ Kaeya ★★★★\n+ Chongyun ★★★★\n+ Diona ★★★★\n+ Rosaria ★★★★\n+ Qiqi ★★★★★\n+ Ganyu ★★★★★\n+ Kamisato Ayaka ★★★★★\n+ Aloy ★★★★★```")
    elif elm == "geo" :
        await ctx.send("```yaml\n\t\t-------- Geo Character Genshin --------\n\n+ Noelle ★★★★\n+ Ningguang ★★★★ \n+ Gorou ★★★★\n+ Zhongli ★★★★★\n+ Albedo ★★★★★```")
    elif elm == "electro" :
        await ctx.send("```yaml\n\t\t-------- Electro Character Genshin --------\n\n+ Lisa ★★★★\n+ Fischl ★★★★ \n+ Razor ★★★★\n+ Beidou ★★★★\n+ Kujou Sara ★★★★\n+ Keqing ★★★★★\n+ Raiden Shogun(Baal) ★★★★★```")
    elif elm == "all" :
        await ctx.send("```yaml\n\t\t-------- All Character Genshin --------\n\nPyro Nation :\n+ Amber ★★★★\n+ Bennet ★★★★ \n+ Xiangling ★★★★\n+ Xinyan ★★★★\n+ yanfei ★★★★\n+ Diluc ★★★★★\n+ Klee ★★★★★\n+ Hu Tao ★★★★★\n+ Yoimiya ★★★★★\nElectro Nation :\n+ Lisa ★★★★\n+ Fischl ★★★★ \n+ Razor ★★★★\n+ Beidou ★★★★\n+ Kujou Sara ★★★★\n+ Keqing ★★★★★\n+ Raiden Shogun(Baal) ★★★★★\nAnemo Nation :\n+ Sucrose ★★★★\n+ Sayu ★★★★ \n+ Jean ★★★★★\n+ venti ★★★★★\n+ Xiao ★★★★★\n+ Kaedehara Kazuha ★★★★★\nCryo Nation :\n+ Kaeya ★★★★\n+ Chongyun ★★★★\n+ Diona ★★★★\n+ Rosaria ★★★★\n+ Qiqi ★★★★★\n+ Ganyu ★★★★★\n+ Kamisato Ayaka ★★★★★\n+ Aloy ★★★★★\nGeo Nation :\n+ Noelle ★★★★\n+ Ningguang ★★★★ \n+ Gorou ★★★★\n+ Zhongli ★★★★★\n+ Albedo ★★★★★```")
    else :
        await ctx.send("```yaml\nElemental Nation Tidak Ditemukan atau huruf tidak tepat (jangan gunakan Caps)```")

@bot.command()
async def talent(ctx,char):
    strings = {"Charged": "Charge",
               "Inherited": "Inhert", "Explosion": "Explsn",
               "Duration": "Drtion", "Stamina": "Stmina",
               "Regeneration": "Regen", "Continuous": "Cont",
               "Spinning": "Spin", "Absorption": "Absorb",
               "Lightning": "Lgtning", "Reduction": "Reduce",
               "Infusion": "Infuse", "Slashing": "Slash",
               "Summoning": "Summon", "Falling": "Fall",
               "Thunder": "Thnder", "Consumption": "Cnsume",
               "Elemental": "Elem", "Entering": "Enter",
               "Exiting": "Exit", "Activation": "Active",
               "Healing": "Heal", "Stiletto": "Stleto",
               "Thunderclap": "Thunder Clap", "Consecutive": "Cont",
               "Conductive": "Cond", "Discharge": "Dchrge", "Illusory": "Illsry",
               "Triggering": "Triger", "Regenerated": "Regen", "Electro": "Elctro",
               "duration": "drtion", "Companion": "Cmpnion", "Additional": "Add",
               "Charging": "Charge", "Tornado": "Trnado", "Meteorite": "Meteor",
               "Shockwave": "Shock Wave", "Stonewall": "Stone Wall",
               "Pyronado": "Pyro nado", "Plunging": "Plunge",
               "Preemptive": "Pre Emptve", "(Ranged)": "Ranged",
               "Resonance": "Reso", "Petrification": "Petri", "Frostflake": "Frost Flake",
               "Transient": "Trans", "Blossom": "Blosom", "Cutting": "Cut",
               "Decrease": "Dcrese", "Scarlet": "Scrlet", "Icewhirl": "Ice Whirl",
               "Grimheart": "Grim Heart", "Physical": "Phys", "Lightfall": "Light Fall",
               "Maximum": "Max", "Abundance": "Abndce", "Kindling": "Kind-ling",
               "Blazing": "Blaze", "PressFuufuu": "Press Fuu Fuu", "Whirlwind": "Whirl Wind",
               "Fuufuu": "Fuu fuu", "Coordinated": "Coor", "Hitotachi": "Hito-tachi",
               "Resolve": "Rsolve", "Restoration": "Rstore", "Titanbreaker": "Titan Breaker",
               "Stormcluster": "Storm Cluster", "Chillwater": "Chill Water",
               "Bomblets": "Bomb-lets", "Rushing": "Rush"}
    i = 0
    type = {
        1: "Basic Attack",
        2: "E Skill",
        3: "Q Burst"
    }
    page = f"https://genshin.honeyhunterworld.com/db/char/{char}"
    response = requests.get(page)
    soup = BeautifulSoup(response.text, 'html.parser')
    headers = []
    datass = []
    if response.status_code == 200:
        tables = soup.find_all("table", {'class': 'add_stat_table'})
        tables.remove(tables[0])
        tables.remove(tables[0])
        if (char=="ayaka" or char=="mona"):
            tables.remove(tables[2])
        a = 3
        b = 0
        while (a > 0):
            tab = tables[b].find_all('tr')
            b += 1
            a -= 1
            c = 0
            header = []
            datas = []
            for tr in tab:
                data = []
                tds = tr.find_all('td')
                d = 0
                for td in tds:
                    temp = ""
                    if (c == 0 and d <= 13):
                        header.append(td.text)
                    elif (d <= 13):
                        temp = td.text
                        for string in strings:
                            temp = temp.replace(string, strings[string])
                        temp = temp.replace(":", "")
                        temp = temp.replace(" ", "\n")
                        temp = temp.replace("-", "\n-\n")
                        temp = temp.replace("/", "\n/\n")
                        temp = temp.replace("×", "\n×\n")
                        if (d == 0):
                            temp = "+" + temp
                        data.append(temp)
                    else:
                        break
                    d += 1
                if (c == 0):
                    headers.append(header)
                else:
                    datas.append(data)
                c += 1
            datass.append(datas)
    for header, datas in zip(headers, datass):
        i+=1
        header.remove(header[3])
        header.remove(header[4])
        header.remove(header[5])
        header.remove(header[9])
        header.remove(header[6])
        header.remove(header[7])
        for data in datas:
            data.remove(data[3])
            data.remove(data[4])
            data.remove(data[5])
            data.remove(data[9])
            data.remove(data[6])
            data.remove(data[7])
        x = (tabulate(datas, header))
        await ctx.send("> **{} {}**\n```yaml\n{}```".format(char,type[i],x))

@bot.command()
async def info(ctx,char):
    '''
        urllib.request.urlretrieve('https://static.wikia.nocookie.net/gensin-impact/images/8/8d/Character_Ganyu_Card.png/revision/latest?cb=20210106062018',"ganyu.png")
        im = Image.open(r"ganyu.png")
        width, height = im.size
        left = 0
        top = 250
        right = width
        bottom = height - 350
        im1 = im.crop((left, top, right, bottom))
        #im1.show()
        '''
    chars = char.replace(' ', '_')
    page = f'https://genshin-impact.fandom.com/wiki/{char}'
    response = requests.get(page)
    counter = 0
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        side_tab = soup.find("aside")
        char_name = side_tab.find("h2", {'data-source': "name"})
        char_title = side_tab.find("h2", {'data-item-name': "secondary_title"})
        first_detail = side_tab.find("tbody")
        rarity = first_detail.find('img')
        ct1 = 0
        char_weap = ""
        char_elem = ""
        for a_head in first_detail.find_all('a'):
            if (str(a_head.text) != ""):
                if (ct1 == 0):
                    char_weap = a_head.text
                else:
                    char_elem = a_head.text
                ct1 += 1

        img_tab = side_tab.find("div", {'class': 'wds-tab__content wds-is-current'})
        char_img = img_tab.find('a')
        second_detail = side_tab.find_all("div", {'class': 'wds-tab__content wds-is-current'})
        for data in second_detail:
            counter += 1
            if (counter == 2):
                second_detail = data
                break
        char_sex = data.find('div', {'data-source': 'sex'})
        char_bd = data.find('div', {'data-source': 'birthday'})
        char_nation = data.find('div', {'data-source': 'region'})
        affs = data.find('div', {'data-source': 'affiliation'})
        char_aff = ""
        ct = 0
        limits = len(affs.find_all('a'))
        for affiliation in affs.find_all('a'):
            ct += 1
            if (ct < limits):
                char_aff += affiliation.text + ", "
            else:
                char_aff += affiliation.text
        colors = {"Pyro": 0xe84833, "Cryo": 0x61f2ff, "Hydro": 0x2372fa, "Electro": 0xa838e8, "Geo": 0xebbb38,
                  "Anemo": 0x38eb71}
        ele_png = {
            "Electro": "https://static.wikia.nocookie.net/gensin-impact/images/7/73/Element_Electro.png/revision/latest/scale-to-width-down/64?cb=20201116063049",
            "Pyro": "https://static.wikia.nocookie.net/gensin-impact/images/e/e8/Element_Pyro.png/revision/latest/scale-to-width-down/64?cb=20201116063114",
            "Hydro": "https://static.wikia.nocookie.net/gensin-impact/images/3/35/Element_Hydro.png/revision/latest/scale-to-width-down/64?cb=20201116063105",
            "Cryo": "https://static.wikia.nocookie.net/gensin-impact/images/8/88/Element_Cryo.png/revision/latest/scale-to-width-down/64?cb=20201116063123",
            "Anemo": "https://static.wikia.nocookie.net/gensin-impact/images/a/a4/Element_Anemo.png/revision/latest/scale-to-width-down/64?cb=20201116063017",
            "Geo": "https://static.wikia.nocookie.net/gensin-impact/images/4/4a/Element_Geo.png/revision/latest/scale-to-width-down/64?cb=20201116063036"}
        embed = discord.Embed(title=char_name.text, description=char_title.text, color=colors[f'{char_elem}'])
        embed.set_author(name="Genshin Impact Fandom", url="https://genshin-impact.fandom.com/",
                         icon_url="https://img.utdstc.com/icon/9a6/3d0/9a63d0817ee337a44e148854654a88fa144cfc6f2c31bc85f860f4a42c92019f:200")
        embed.add_field(name="Rarity", value=rarity['title'], inline=True)
        embed.add_field(name="Weapon", value=char_weap, inline=True)
        embed.add_field(name="Element", value=char_elem, inline=True)
        embed.add_field(name="Nation", value=char_nation.find('div').text, inline=True)
        embed.add_field(name="Sex", value=char_sex.find('a').text, inline=True)
        embed.add_field(name="Birthday", value=char_bd.find('div').text, inline=True)
        embed.add_field(name="Affiliation", value=char_aff, inline=False)
        # embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
        # embed.set_thumbnail(url=f"{ctx.guild.icon}")
        embed.set_thumbnail(url=ele_png[f'{char_elem}'])
        embed.set_image(url=f"{char_img['href']}")
        embed.set_footer(text="~~~Ganyu yang paling cantik euy~~~")
        await ctx.send(embed=embed)
    else:
        print("Karakter Tidak Ditemukan, Periksa kembali nama karakter yang di input")

@bot.command()
async def event(ctx):
    titles, imgs, durations, event_type = event_news(0)
    if len(titles) == 0:
        print("Data tidak tersedia, atau terjadi bug pada bot, harap hubungi developer")
    else:
        for idx in range(len(titles)):
            embed = discord.Embed(title=titles[idx], description=durations[idx], color=0x38eb71)
            embed.set_author(name="Genshin Impact Fandom", url="https://genshin-impact.fandom.com/",
                             icon_url="https://img.utdstc.com/icon/9a6/3d0/9a63d0817ee337a44e148854654a88fa144cfc6f2c31bc85f860f4a42c92019f:200")
            embed.add_field(name="Event Type", value=event_type[idx], inline=True)
            embed.set_image(url=imgs[idx])
            await ctx.send(embed=embed)

@bot.command()
async def upcoming_event(ctx):
    titles, imgs, durations, event_type = event_news(1)
    if len(titles) == 1:
        print("Data tidak tersedia, atau terjadi bug pada bot, harap hubungi developer")
    else :
        for idx in range(len(titles)):
            embed = discord.Embed(title=titles[idx], description=durations[idx], color=0x38eb71)
            embed.set_author(name="Genshin Impact Fandom", url="https://genshin-impact.fandom.com/",
                             icon_url="https://img.utdstc.com/icon/9a6/3d0/9a63d0817ee337a44e148854654a88fa144cfc6f2c31bc85f860f4a42c92019f:200")
            embed.add_field(name="Event Type", value=event_type[idx], inline=True)
            embed.set_image(url=imgs[idx])
            await ctx.send(embed=embed)

@bot.command()
async def nonton(ctx,*tags):
    list_hal = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']
    tags=list(str(tags))
    print(tags)
    hal=random.randint(1,15)
    search = ""
    #if tags[0] in list_hal:
        #hal = int(tags[0])
        #tags = tags.remove(tags[0])
    for i in range(len(tags)):
        search += tags[i]+"+"
    print(search)
    page = requests.get(f'https://www.google.com/search?q=youtube+{search}')
    soup = BeautifulSoup(page.text, 'html.parser')
    counter = 0
    format = 47
    if page.status_code == 200:
        str_soup = str(soup)
        list_link = []

        link = ""
        parser = str_soup.find("https://www.youtube.com/watch")
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
    await ctx.send(list_link[hal])


@bot.command()
async def wp(ctx, weap):
    weaps = weap.replace(' ','_')
    page = f'https://genshin-impact.fandom.com/wiki/{weaps}'
    response = requests.get(page)
    counter = 0
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        a = soup.find('aside')

        fg = a.find('figure')
        img = fg.find('a', {'class': 'image image-thumbnail'})
        gmbr = img.find('img')
        img_link = gmbr['src']
        print(img_link)
        name = weap

        div1 = a.find('div', {'data-source': 'type'})
        type = div1.find('a')
        print(type.text)

        div2 = a.find('div', {'data-source': 'rarity'})
        rar = div2.find('img')
        rarity = rar['title']
        print(rarity)

        div3 = a.find('section', {'class': 'pi-item pi-group pi-border-color'})
        st = div3.find('table')
        tab = st.find('tbody')
        stat = tab.find_all('td')
        print(stat[0].text)
        print(stat[1].text)
        print(stat[2].text)

        div4 = a.find('section', {'class': 'pi-item pi-panel pi-border-color wds-tabber'})
        desk = div4.find('table')

        head = desk.find('thead')
        th = head.find('th')
        header = th.text

        body = desk.find('tbody')
        td = body.find('td')
        print(td.text)

        wpc = {"Sword": 0xe84833, "Claymore": 0x2372fa, "Polearm": 0xebbb38, "Catalyst": 0xa838e8, "Bow": 0x38eb71}
        logo = {
            "Sword": "https://static.wikia.nocookie.net/gensin-impact/images/8/81/Icon_Sword.png/revision/latest/scale-to-width-down/128?cb=20210413210800",
            "Claymore": "https://static.wikia.nocookie.net/gensin-impact/images/6/66/Icon_Claymore.png/revision/latest?cb=20210413210803",
            "Polearm": "https://static.wikia.nocookie.net/gensin-impact/images/6/6a/Icon_Polearm.png/revision/latest?cb=20210413210804",
            "Catalyst": "https://static.wikia.nocookie.net/gensin-impact/images/2/27/Icon_Catalyst.png/revision/latest?cb=20210413210802",
            "Bow": "https://static.wikia.nocookie.net/gensin-impact/images/8/81/Icon_Bow.png/revision/latest?cb=20210413210801"}

        embed = discord.Embed(title=name, color=wpc[f'{type.text}'])
        embed.set_author(name="Genshin Impact Fandom", url="https://genshin-impact.fandom.com/",
                         icon_url="https://img.utdstc.com/icon/9a6/3d0/9a63d0817ee337a44e148854654a88fa144cfc6f2c31bc85f860f4a42c92019f:200")
        embed.add_field(name="Weapon Type", value=type.text, inline=True)
        embed.add_field(name="Rarity", value=rarity, inline=True)
        embed.add_field(name="Base ATK lvl1", value=stat[0].text, inline=False)
        embed.add_field(name="Sec Stat Type", value=stat[1].text, inline=True)
        embed.add_field(name="Sec Stat lvl1", value=stat[2].text, inline=True)
        embed.add_field(name=th.text, value=td.text, inline=False)
        # embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
        # embed.set_thumbnail(url=f"{ctx.guild.icon}")
        embed.set_thumbnail(url=logo[f'{type.text}'])
        embed.set_image(url=f"{img_link}")
        await ctx.send(embed=embed)

bot.run("InsertTokenHere")
