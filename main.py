import discord, random, requests
from bs4 import BeautifulSoup
from discord.ext import commands
from tabulate import tabulate
from command.eventnews import event_news
from command.weapondesc import weapon_desc
from command.ytsearch import youtube_video
from command.charinfo import char_info

from data.strings_data import data
from utils.get_gelImage import get_gelImage

# tkn = os.environ['tok']
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents)

bot.remove_command('help')


@bot.event
async def on_ready():
    print('{0.user} ready to go for new Adventure!'.format(bot))


@bot.command()
async def ping(ctx):
    await ctx.send(f'Hello Traveler! [{round(bot.latency * 1000)}ms]')


@bot.command()
async def helps(ctx):
    notes_data = data()
    await ctx.send(notes_data.notes)


@bot.command()
async def calcdmg(ctx, att, cd, ability, elebonus):
    res = int(att) * (float(ability) / 100) * (float(elebonus) / 100) * (1 + float(cd) / 100)
    bsra = " Besar Attack = " + str(int(att))
    crd = " Besar Critical damage = " + str(cd) + "%"
    elmb = " Besar Elemental Bonus = " + str(elebonus) + "%"
    talt = " Talent Damage = " + str(ability) + "%"
    a = " Total Damage yang diperoleh = " + str(int(res))
    output = "```yaml\n+{}\n+{}\n+{}\n+{}\n+{}```".format(bsra, crd, elmb, talt, a)
    await ctx.send(output)


@bot.command()
async def calcresin(ctx, a, b):
    timestart = float(a)
    wktm = "Waktu Mulai : " + str(timestart)
    timeend = float(b)
    wkta = "Waktu Akhir : " + str(timeend)
    menit1 = abs((int(timeend) - int(timestart)) * 60)
    menit2 = ((timeend % 1) - (timestart % 1)) * 100
    res = int((menit1 + menit2) / 8)
    total = "Resin yang didapat : " + str(res)

    await ctx.send("```yaml\n+{}\n+{}\n+{}```".format(wktm, wkta, total))


@bot.command()
async def calcprim(ctx, hr, evnt, blessing):
    abs_init = 600
    if (int(blessing) > int(hr)):
        blessing = hr
    res = (60 * int(hr)) + (90 * int(blessing))
    daily = " Daily = " + hr + " x " + str(60) + " = " + str(60 * int(hr)) + "\n"
    event = " Event bulanan = " + evnt + " x " + str(420) + " = " + str(int(evnt) * 420) + "\n"
    abs = " Abyss Floor = " + str(abs_init + (int(int(hr) / 14) * 600)) + "\n"
    blss = " Blessing = " + blessing + " x " + str(90) + " = " + str(90 * int(blessing)) + "\n"
    mix = " Total primogem = " + str(res + abs_init + (int(int(hr) / 14) * 600) + int(evnt) * 420)
    output = "```yaml\n+{}+{}+{}+{}+{}```".format(daily, event, abs, blss, mix)
    await ctx.send(output)


# ---------------- img bot ------------------
@bot.command()
async def pics(ctx, *tags):
    """Calls get_gelImage() with tags specified by user, then sends an image."""

    img = get_gelImage(tags)

    if "rq" in tags or "re" in tags:
        if ctx.channel.is_nsfw():  # check if channel is suitable for given rating
            return await ctx.send(img)
        else:
            message = "For rating questionable or explicit NSFW channel is required!"
            return await ctx.send(message)

    await ctx.send(img)


@bot.command()
async def maps(ctx):
    await ctx.send(
        "```yaml\n\t\t\t\t-------- Map Farm Genshin Impact --------\n\ncopy link : https://webstatic-sea.mihoyo.com/app/ys-map-sea/?lang=id-id#```")


@bot.command()
async def charlist(ctx, elm):
    if elm == "pyro":
        await ctx.send(
            "```yaml\n\t\t-------- Pyro Character Genshin --------\n\n+ Amber ★★★★\n+ Bennet ★★★★ \n+ Xiangling ★★★★\n+ Xinyann ★★★★\n+ yanfei ★★★★\n+ Diluc ★★★★★\n+ Klee ★★★★★\n+ Hu Tao ★★★★★\n+ Yoimiya ★★★★★```")
    elif elm == "anemo":
        await ctx.send(
            "```yaml\n\t\t-------- anemo Character Genshin --------\n\n+ Sucrose ★★★★\n+ Sayu ★★★★ \n+ Jean ★★★★★\n+ venti ★★★★★\n+ Xiao ★★★★★\n+ Kaedehara Kazuha ★★★★★```")
    elif elm == "cryo":
        await ctx.send(
            "```yaml\n\t\t-------- Cryo Character Genshin --------\n\n+ Kaeya ★★★★\n+ Chongyun ★★★★\n+ Diona ★★★★\n+ Rosaria ★★★★\n+ Qiqi ★★★★★\n+ Ganyu ★★★★★\n+ Kamisato Ayaka ★★★★★\n+ Aloy ★★★★★```")
    elif elm == "geo":
        await ctx.send(
            "```yaml\n\t\t-------- Geo Character Genshin --------\n\n+ Noelle ★★★★\n+ Ningguang ★★★★ \n+ Gorou ★★★★\n+ Zhongli ★★★★★\n+ Albedo ★★★★★```")
    elif elm == "electro":
        await ctx.send(
            "```yaml\n\t\t-------- Electro Character Genshin --------\n\n+ Lisa ★★★★\n+ Fischl ★★★★ \n+ Razor ★★★★\n+ Beidou ★★★★\n+ Kujou Sara ★★★★\n+ Keqing ★★★★★\n+ Raiden Shogun(Baal) ★★★★★```")
    elif elm == "all":
        await ctx.send(
            "```yaml\n\t\t-------- All Character Genshin --------\n\nPyro Nation :\n+ Amber ★★★★\n+ Bennet ★★★★ \n+ Xiangling ★★★★\n+ Xinyan ★★★★\n+ yanfei ★★★★\n+ Diluc ★★★★★\n+ Klee ★★★★★\n+ Hu Tao ★★★★★\n+ Yoimiya ★★★★★\nElectro Nation :\n+ Lisa ★★★★\n+ Fischl ★★★★ \n+ Razor ★★★★\n+ Beidou ★★★★\n+ Kujou Sara ★★★★\n+ Keqing ★★★★★\n+ Raiden Shogun(Baal) ★★★★★\nAnemo Nation :\n+ Sucrose ★★★★\n+ Sayu ★★★★ \n+ Jean ★★★★★\n+ venti ★★★★★\n+ Xiao ★★★★★\n+ Kaedehara Kazuha ★★★★★\nCryo Nation :\n+ Kaeya ★★★★\n+ Chongyun ★★★★\n+ Diona ★★★★\n+ Rosaria ★★★★\n+ Qiqi ★★★★★\n+ Ganyu ★★★★★\n+ Kamisato Ayaka ★★★★★\n+ Aloy ★★★★★\nGeo Nation :\n+ Noelle ★★★★\n+ Ningguang ★★★★ \n+ Gorou ★★★★\n+ Zhongli ★★★★★\n+ Albedo ★★★★★```")
    else:
        await ctx.send("```yaml\nElemental Nation Tidak Ditemukan atau huruf tidak tepat (jangan gunakan Caps)```")

#--------------------------------------------------------------------------------------------------------------------
#-----------------------------------HARUS DI MAINTENANCE DLU, MASIH BUG----------------------------------------------
#--------------------------------------------------------------------------------------------------------------------


@bot.command()
async def talent(ctx, char):
    strings = data().abbrevation()
    i = 0
    type = data.char_skills
    page = f"https://genshin.honeyhunterworld.com/db/char/{char}"
    response = requests.get(page)
    soup = BeautifulSoup(response.text, 'html.parser')
    headers = []
    datass = []
    if response.status_code == 200:
        tables = soup.find_all("table", {'class': 'add_stat_table'})
        tables.remove(tables[0])
        tables.remove(tables[0])
        if (char == "ayaka" or char == "mona"):
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
                    if c == 0 and d <= 13:
                        header.append(td.text)
                    elif d <= 13:
                        temp = td.text
                        for string in strings:
                            temp = temp.replace(string, strings[string])
                        temp = temp.replace(":", "")
                        temp = temp.replace(" ", "\n")
                        temp = temp.replace("-", "\n-\n")
                        temp = temp.replace("/", "\n/\n")
                        temp = temp.replace("×", "\n×\n")
                        if d == 0:
                            temp = "+" + temp
                        data.append(temp)
                    else:
                        break
                    d += 1
                if c == 0:
                    headers.append(header)
                else:
                    datas.append(data)
                c += 1
            datass.append(datas)
    for header, datas in zip(headers, datass):
        i += 1
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
        await ctx.send("> **{} {}**\n```yaml\n{}```".format(char, type[i], x))

#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------

@bot.command()
async def info(ctx, char_query):
    """
        urllib.request.urlretrieve('https://static.wikia.nocookie.net/gensin-impact/images/8/8d/Character_Ganyu_Card.png/revision/latest?cb=20210106062018',"ganyu.png")
        im = Image.open(r"ganyu.png")
        width, height = im.size
        left = 0
        top = 250
        right = width
        bottom = height - 350
        im1 = im.crop((left, top, right, bottom))
        #im1.show()
    """
    char = char_info(char_query)
    if char is not None:

        colors = data.elemental_color
        ele_png = data.elemental_images
        embed = discord.Embed(title=char.char_name, description=char.char_title, color=colors[char.char_element])
        embed.set_author(name="Genshin Impact Fandom", url="https://genshin-impact.fandom.com/",
                         icon_url="https://img.utdstc.com/icon/9a6/3d0/9a63d0817ee337a44e148854654a88fa144cfc6f2c31bc85f860f4a42c92019f:200")
        embed.add_field(name="Rarity", value=char.char_rarity, inline=True)
        embed.add_field(name="Weapon", value=char.char_weap, inline=True)
        embed.add_field(name="Element", value=char.char_element, inline=True)
        embed.add_field(name="Nation", value=char.char_nation, inline=True)
        embed.add_field(name="Sex", value=char.char_sex, inline=True)
        embed.add_field(name="Birthday", value=char.char_bday, inline=True)
        embed.add_field(name="Affiliation", value=char.char_affiliation, inline=False)
        embed.set_thumbnail(url=ele_png[char.char_element])
        embed.set_image(url=char.char_img)
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
async def nonton(ctx, *tags):

    tags = list(str(tags))
    search = ""
    for i in range(len(tags)):
        search += tags[i] + "+"

    list_link = youtube_video(search)

    if list_link is not None :
        hal = random.randint(1, 15)
        await ctx.send(list_link[hal])
    else:
        print("Data tidak tersedia, atau terjadi bug pada bot, harap hubungi developer")


@bot.command()
async def wp(ctx, weap):
    weapon = weapon_desc(weap)
    if weapon is not None:
        wpc = data().weapon_type_color
        logo = data().weapon_type_imgs

        embed = discord.Embed(title=weapon.weapon_name, color=wpc[f'{weapon.weapon_type}'])
        embed.set_author(name="Genshin Impact Fandom", url="https://genshin-impact.fandom.com/",
                         icon_url="https://img.utdstc.com/icon/9a6/3d0/9a63d0817ee337a44e148854654a88fa144cfc6f2c31bc85f860f4a42c92019f:200")
        embed.add_field(name="Weapon Type", value=weapon.weapon_type, inline=True)
        embed.add_field(name="Rarity", value=weapon.weapon_rarity, inline=True)
        embed.add_field(name="Base ATK lvl1", value=weapon.weapon_base_atk, inline=False)
        embed.add_field(name="Sec Stat Type", value=weapon.weapon_stat_type, inline=True)
        embed.add_field(name="Sec Stat lvl1", value=weapon.weapon_stat_base, inline=True)
        embed.add_field(name=weapon.weapon_desc_title, value=weapon.weapon_desc, inline=False)
        # embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
        # embed.set_thumbnail(url=f"{ctx.guild.icon}")
        embed.set_thumbnail(url=logo[f'{weapon.weapon_type}'])
        embed.set_image(url=f"{weapon.weapon_img_link}")

        await ctx.send(embed=embed)
    else:
        print("Data tidak tersedia, atau terjadi bug pada bot, harap hubungi developer")


bot.run("InsertTokenHere")
