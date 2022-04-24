from bs4 import BeautifulSoup as bs
import requests

def get_soup(url):
    return bs(requests.get(url).text, "html.parser")

temp = list(get_soup("http://dnd5e.wikidot.com").find_all("a")) 

temp = [x for x in temp if str(x.get("href"))[0] == "/"]

background = [x for x in temp if "background:" in str(x.get("href"))]

feats = [x for x in temp if "feat:" in str(x.get("href"))]

for a,b in enumerate(temp):
    print(f"{a}: {b}")
print("\nbackgrounds\n")
with open("backgrounds.json", "w") as data:
    data.write('{"backgrounds":[')
    m = len(background)
    for a,b in enumerate(background): #needs source
        href = b["href"]
        link = f"http://dnd5e.wikidot.com{href}"
        bg = get_soup(link)
        content = list(bg.find("div", {"class":"main-content"}).find_all("p"))
        for x in content:
            if "Source:" in x.text:
                source = x.text.replace("Source: ", "")
                if "Hoard of the Dragon Queen" in source: #this is because backgrounds from hoard of the dragon queen has additional text
                    source = "Hoard of the Dragon Queen"
                break
        data.write("\n    {"+f'"name":"{b.text}", "link":"{link}", "source":"{source}"'+"}" + f"{',' if a!=m-1 else ''}")
        print(" creating:   [" + "#"*int((a+1)/m*10) + "  "*(10-int((a+1)/m*10)) + "]    {:03d}% ".format(int((a+1)/m*100)), end='\r')
    
    data.write("\n]}")

print("\nfeats\n")
with open("feats.json", "w") as data:
    data.write('{"feats":[')
    for a,b in enumerate(feats): #needs prerequisite and source
        href = b["href"]
        data.write("\n    {"+f'"name":"{b.text}", "source":"http://dnd5e.wikidot.com{href}"'+"}" + f"{',' if a!=len(feats)-1 else ''}")
    data.write("\n]}")