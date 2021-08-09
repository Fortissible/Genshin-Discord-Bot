import os
import discord
import requests
import json
from discord.ext import commands
import random

#tkn = os.environ['tok']

bot = commands.Bot(command_prefix='~')

notes = "\n**Command prefix [~]**\n\n**List Command**\n\n~ping      : ngecek ping```yaml\ncontoh : ~ping```~calcdmg   : [attack][critdmg%][talentattack%][elebonus%]```yaml\ncontoh : ~calcdmg 2109 150.7 704.2 45.6```~calcresin : [timestart][timeend]```yaml\ncontoh : ~calcresin 17.44 22.20```~pics       : [chara][*(series)][/tags]```yaml\ncontoh : ~pics ganyu (genshin impact)\ncontoh : ~pics ganyu (genshin impact)/office\ncontoh : ~pics mona (genshin impact)/swimsuit\ncontoh : ~pics hatsune miku/swimsuit\n* optional```~calcprim   : [Primogem/hari] [Jumlah Hari] [Banyak event/bulan] ```yaml\ncontoh : ~calcprim 60 15 1```"
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

    # make tags suitable for Gelbooru API url
    formatted_tags = "_".join(tags).replace("/","+")

    print(rating, formatted_tags)

    '''
    api_url = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=50&tags={rating}+{formatted_tags}"
    '''
    api_url = f"https://danbooru.donmai.us/posts.json?tags={rating}+{formatted_tags}"
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

# ---------------- img bot ------------------

@bot.command()
async def pics(ctx, *tags):
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
async def calcprim(ctx, prgm, hr, evnt):
  res = int(prgm) * (int(hr))
  event = " ditambah Event bulanan = " + str(int(evnt)*420)
  abs   = " ditambah Abyss Floor bulanan = 600"
  blss  = " ditambah blessing = " + str(int(hr)*90)
  mix   = "total primogem = " + str(res) + event + abs + blss
  await ctx.send(mix)

bot.run("InsertTokenHere")
