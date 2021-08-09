import os
import discord
from bs4 import BeautifulSoup
import requests
import json
from discord.ext import commands
import random
from tabulate import tabulate

#tkn = os.environ['tok']

bot = commands.Bot(command_prefix='~')

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
        "contoh : ~talent ayaka```"

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
async def calcdmg(ctx,att,cd,ability,elebonus):
  res = int(att) * float(ability)/100 * (1 + float(cd)/100) * (1 + float(elebonus)/100)
  a = " Total Damage yang diperoleh = " + str(res)
  output = "```yaml\n+{}```".format(a)
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
  mix   = " Total primogem = " + str( res + absinit + (int(int(hr)/14)*600) + int(evnt)*420)
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
                        temp = td.text.replace(" ", "\n")
                        temp = temp.replace("-", "-\n")
                        temp = temp.replace("/", "\n/")
                        temp = temp.replace("×", "\n×")
                        temp = temp.replace(":", "")
                        if (d==0):
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
        
bot.run("InsertTokenHere")
