from bs4 import BeautifulSoup as bs
import requests
import os

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
    for a,b in enumerate(background): #needs source
        href = b["href"]
        data.write("\n    {"+f'"name":"{b.text}", "source":"http://dnd5e.wikidot.com{href}"'+"}" + f"{',' if a!=len(background)-1 else ''}")
    data.write("\n]}")

print("\nfeats\n")
with open("feats.json", "w") as data:
    data.write('{"feats":[')
    for a,b in enumerate(feats): #needs prerequisite and source
        href = b["href"]
        data.write("\n    {"+f'"name":"{b.text}", "source":"http://dnd5e.wikidot.com{href}"'+"}" + f"{',' if a!=len(feats)-1 else ''}")
    data.write("\n]}")