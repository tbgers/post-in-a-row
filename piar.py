import json
import lxml
import requests
import time
from bs4 import BeautifulSoup

start_time = time.time()

def get_pages():
    html = requests.get(f"https://tbgforums.com/forums/viewtopic.php?id=190")
    src = html.content
    soup = BeautifulSoup(src, 'lxml')
    pages = soup.find("p", class_="pagelink conl")
    return int(pages.find_all("a")[-2].text)

def get_posters(page):
    users = []
    try:
        html = requests.get(f"https://tbgforums.com/forums/viewtopic.php?id=190&p={page}")
        src = html.content
        soup = BeautifulSoup(src, 'lxml')
        posts = soup.find_all("div")
        for i in posts:
            if i.has_attr("class"):
                if "blockpost" in i["class"]:
                    content = i.find(class_="postbody")
                    users.append(content.find_all("dt")[0].get_text())
        print(f"{page}: Found")
        return users
    except AttributeError:
        print(f"{page}: Not found.")

def get_scores(count):
    scoreboard = []
    pending_score = 0
    for i in range(1, count+1):
        scoreboard += get_posters(i)
    return scoreboard

def match(txt, standard : int):
    for i in range(standard - len(str(txt))):
        txt = str(txt) + (" ")
    return txt

pages = get_pages()
leaderboard = {}
x = get_scores(pages)

pending_score = 1
for i in range(len(x)):
    if x[i] not in leaderboard.keys():
        leaderboard[x[i]] = 0
    if x[i] != x[i - 1] and i != 0:
        leaderboard[x[i - 1]] = max(leaderboard[x[i - 1]], pending_score)
        pending_score = 1
    else:
        pending_score += 1


leaderboard = {k: v for k, v in sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)}

j = 0
for i in leaderboard.keys():
    j += 1
    print(f"{match(j, 3)} | {match(i, 25)} | {match(leaderboard[i], 4)}")
