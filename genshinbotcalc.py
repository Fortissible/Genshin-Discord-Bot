import os
import discord
import requests
import json
from discord.ext import commands
import random

#tkn = os.environ['tok']

bot = commands.Bot(command_prefix='~')

notes = "\n**Command prefix [~]**\n\n**List Command**\n\n~ping      : ngecek ping```yaml\ncontoh : ~ping```~calcdmg   : [attack][critdmg%][talentattack%][elebonus%]```yaml\ncontoh : ~calcdmg 2109 150.7 704.2 45.6```~calcresin : [timestart][timeend]```yaml\ncontoh : ~calcresin 17.44 22.20```~pics       : [chara][*(series)][/tags]```yaml\ncontoh : ~pics ganyu (genshin impact)\ncontoh : ~pics ganyu (genshin impact)/office\ncontoh : ~pics mona (genshin impact)/swimsuit\ncontoh : ~pics hatsune miku/swimsuit\n* optional```~calcprim   : [Jumlah Hari] [Banyak event/bulan] [Durasi Blessing(hari)] ```yaml\ncontoh : ~calcprim 60 15 1```~maps : Map untuk Farm apapun```yaml\ncontoh : ~maps```~charlist   : [element atau all]```yaml\ncontoh : ~charlist anemo    ~charlist all```"
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


bot.run("InsertTokenHere")
