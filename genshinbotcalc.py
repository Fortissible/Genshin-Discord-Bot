import os
import discord
import requests
import json
from discord.ext import commands
import random

#tkn = os.environ['tok']

bot = commands.Bot(command_prefix='~')

notes = "\n**Command prefix [~]**\n\n**List Command**\n\n~ping      : ngecek ping```yaml\ncontoh : ~ping```~calcdmg   : [attack][critdmg%][talentattack%][elebonus%]```yaml\ncontoh : ~calcdmg 2109 150.7 704.2 45.6```~calcresin : [timestart][timeend]```yaml\ncontoh : ~calcresin 17.44 22.20```~pics       : [chara][*(series)][/tags]```yaml\ncontoh : ~pics ganyu (genshin impact)\ncontoh : ~pics ganyu (genshin impact)/office\ncontoh : ~pics mona (genshin impact)/swimsuit\ncontoh : ~pics hatsune miku/swimsuit\n* optional```~calcprim   : [Jumlah Hari] [Banyak event/bulan] [Durasi Blessing(hari)] ```yaml\ncontoh : ~calcprim 60 15 1```"
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
  await ctx.send(res)

@bot.command()
async def calcresin(ctx,a,b):
  timestart=float(a)
  timeend = float(b)
  menit1 = abs((int(timeend)-int(timestart))*60)
  menit2 = ((timeend%1)-(timestart%1))*100
  res = int((menit1+menit2)/8)
  await ctx.send("Total Resin = "+str(res))

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

bot.run("InsertTokenHere")
