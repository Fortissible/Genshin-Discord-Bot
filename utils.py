import json
import random
import requests


class data:
    def __init__(self):
        self.notes = "\n**Command prefix [~]**" \
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
                     "contoh : ~charlist anemo    ~charlist all```" \
                     "~talent : [char]" \
                     "```yaml\n" \
                     "contoh : ~talent ayaka```" \
                     "~info  : [Nama Character] (Jika lebih dari 1 kata gunakan Underline'_') " \
                     "```yaml\n" \
                     "contoh : ~info Hu_Tao```" \
                     "~nonton : [Nama Video] " \
                     "```yaml\n" \
                     "contoh : ~nonton Ganyu wangi```" \
                     "~wp : [Nama Weapon] (Jika lebih dari 1 kata gunakan Underline'_')" \
                     "```yaml\n" \
                     "contoh : ~wp Skyward_Harp```"
        self.abbrevation = {"Charged": "Charge",
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
        self.char_skills = {
            1: "Basic Attack",
            2: "E Skill",
            3: "Q Burst"
        }
        self.elemental_images = {
            "Electro": "https://static.wikia.nocookie.net/gensin-impact/images/7/73/Element_Electro.png/revision/latest/scale-to-width-down/64?cb=20201116063049",
            "Pyro": "https://static.wikia.nocookie.net/gensin-impact/images/e/e8/Element_Pyro.png/revision/latest/scale-to-width-down/64?cb=20201116063114",
            "Hydro": "https://static.wikia.nocookie.net/gensin-impact/images/3/35/Element_Hydro.png/revision/latest/scale-to-width-down/64?cb=20201116063105",
            "Cryo": "https://static.wikia.nocookie.net/gensin-impact/images/8/88/Element_Cryo.png/revision/latest/scale-to-width-down/64?cb=20201116063123",
            "Anemo": "https://static.wikia.nocookie.net/gensin-impact/images/a/a4/Element_Anemo.png/revision/latest/scale-to-width-down/64?cb=20201116063017",
            "Geo": "https://static.wikia.nocookie.net/gensin-impact/images/4/4a/Element_Geo.png/revision/latest/scale-to-width-down/64?cb=20201116063036"}
        self.elemental_color = {"Pyro": 0xe84833, "Cryo": 0x61f2ff, "Hydro": 0x2372fa, "Electro": 0xa838e8,
                                "Geo": 0xebbb38,
                                "Anemo": 0x38eb71}
        self.weapon_type_color = {"Sword": 0xe84833, "Claymore": 0x2372fa, "Polearm": 0xebbb38, "Catalyst": 0xa838e8,
                                  "Bow": 0x38eb71}
        self.weapon_type_imgs = {
            "Sword": "https://static.wikia.nocookie.net/gensin-impact/images/8/81/Icon_Sword.png/revision/latest/scale-to-width-down/128?cb=20210413210800",
            "Claymore": "https://static.wikia.nocookie.net/gensin-impact/images/6/66/Icon_Claymore.png/revision/latest?cb=20210413210803",
            "Polearm": "https://static.wikia.nocookie.net/gensin-impact/images/6/6a/Icon_Polearm.png/revision/latest?cb=20210413210804",
            "Catalyst": "https://static.wikia.nocookie.net/gensin-impact/images/2/27/Icon_Catalyst.png/revision/latest?cb=20210413210802",
            "Bow": "https://static.wikia.nocookie.net/gensin-impact/images/8/81/Icon_Bow.png/revision/latest?cb=20210413210801"}


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

    if (tags[len(tags) - 1]).isdigit():
        halaman = tags[len(tags) - 1]
        tags.remove(tags[len(tags) - 1])
    else:
        halaman = '1'

    # make tags suitable for Gelbooru API url
    formatted_tags = "_".join(tags).replace("/", "+")

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
