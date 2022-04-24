from bs4 import BeautifulSoup as bs
import requests

def get_soup(url):
    return bs(requests.get(url).text, "html.parser")

temp = list(get_soup("http://dnd5e.wikidot.com/spells").find_all("a")) 

spells = [x for x in temp if "spell:" in str(x.get("href"))]
with open("spells.json", "w") as data:
    data.write('{"spells":{')
    for w,x in enumerate(spells):
        href = x["href"]
        text = get_soup(f"http://dnd5e.wikidot.com{href}").find("div", {"id": "page-content"})
        permalink = f"http://dnd5e.wikidot.com{href}"
        desc = list(text.find_all("p"))
        print(x.text + "\n")
        #print("\n\n".join([f'{x}: {y.text}' for x,y in enumerate(desc)]))    
        level = desc[1].text
        try:
            school = level[10:]
            level = int(level[0])
        except Exception:
            school = level.replace("cantrip", "")
            level = 0
        if "(ritual)" in school.lower():
            school.replace("(ritual)", "")
            ritual = 'true'
        else:
            ritual = 'false'
        if "(technomagic)" in school.lower():
            school.replace("(technomagic)", "")
            technomagic = 'true'
        else:
            technomagic = 'false'
        temp = desc[2].text.split("\n")
        castTime = temp[0].replace("Casting time: ","")
        spellRange = temp[1].replace("Range: ","")
        components = temp[2].replace("Components: ","").split(",")
        components = "["+",".join([f'"{x}"' for x in components]) + "]"
        duration = temp[3].replace("Duration: ","")
        data.write(f'\n    "{x.text}"' + ":{" + f'"source":"{desc[0].text.replace("Source: ","")}", "level":{level}, "school":"{school}", "ritual":{ritual}, "technomagic":{technomagic}, "duration":"{duration}", "range":"{spellRange}", "components":{components}, "time":"{castTime}", "link":"{permalink}"' + "}"+ f'{"," if w!=len(spells)-1 else ""}')
    data.write("\n}}")