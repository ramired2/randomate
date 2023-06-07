import requests
from bs4 import BeautifulSoup
# import os
from requests.sessions import Request
from urllib.request import urlopen, Request
import json

# CHART WEBSCRAPE
def billboardCategories():
    URL ="https://www.billboard.com/charts/"
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})

    infos = []

    webpage = urlopen(req).read()

    soup = BeautifulSoup(webpage, 'html.parser')

    # links = soup.find_all("div", class_ = "o-chart-list-card")
    links = []
    # category links
    for indiv in soup.find_all("a", class_ = "lrv-u-flex", href=True):
        if "https" not in indiv['href'] and "#" not in indiv['href']:
            links.append(indiv['href'])    

    # print("links:\n")
    # print(links)

    # category names
    for indiv in soup.find_all("span", class_ = "c-span"):
        # print(indiv, '\n')
        infos.append(indiv.get_text())

    #first is "categories"
    infos.pop(0)
    
    
    final = []

    for (indiv, link) in zip(infos, links):
        # PARSE THRU
        indiv = indiv.replace("\n\n\tCategory:\n", "")
        indiv = indiv.replace("\n\n\tLoad More\n", "")
        indiv = indiv.replace("\n\n\tVideo\n", "")
        indiv = indiv.replace('\n', "")
        indiv = indiv.replace('\t', "")

        if "album" not in indiv and "album" not in link:
            if "artist" not in indiv:
                final.append({"category":indiv, "link":link.lower()})
    
    final.append({"category":"Billboard global 200", "link":"/charts/billboard-global-200"})
    
    # print("final list\n")
    # print (final)

    # add to json file
    jsonStr = json.dumps(final, indent=4)
    jsonFile = open("categories.json", "w")
    jsonFile.write(jsonStr)
    jsonFile.close()

    return final

# GETTING CHART INFO WEBSCRAPE
def billboardTracks(category, n):
    print(category, n)


    URL = "https://www.billboard.com" + category
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(req).read()

    soup = BeautifulSoup(webpage, 'html.parser')

    temp = []
    for song in soup.find_all("h3", id="title-of-a-story", class_="a-font-primary-bold-s"):
        if "Gains in Weekly Performance" not in song.get_text() and "Additional Awards" not in song.get_text():
            temp.append(song.get_text())

    #parse thru the songs for \n\t
    songs = []
    for song in temp:
        song = song.replace('\n\n\t\n\t\n\t\t\n\t\t\t\t\t', '')
        song = song.replace('\t\t\n\t\n', '')
        song = song.replace('\t', '')
        song = song.replace('\n', '')

        songs.append(song)

    artists = []
    #getting artists 
    for artist in soup.find_all("span", class_="a-no-trucate"):
        artist = artist.get_text().replace('\n\t\n\t', '')
        artist = artist.replace('\n', '')
        artists.append(artist)

    #json ify it 
    i = 0
    jsonify = []

    if n:
        while i < n:
            jsonify.append({"rank":i+1, "song":songs[i], "artist":artists[i]})
            i+= 1
    else:
        for (song, artist) in zip(songs, artists):
            jsonify.append({"rank":i+1, "song":song, "artist":artist})
            i+= 1

    
    jsonStr = json.dumps(jsonify, indent=4)
    jsonFile = open("rankings.json", "w")
    jsonFile.write(jsonStr)
    jsonFile.close()

    return jsonify

def categoryLinkToTitle(link):
    with open("categories.json", 'r') as l:
        category = json.loads(l.read())

    for i in category:
        # print(i["link"])
        if (link == i["link"]):
             return print(i["category"])

def read(country, n):
    # URL ="https://www.spotifycharts.com/regional/" + country + "/daily/latest"
    # req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})

    # infos = []

    # webpage = urlopen(req).read()

    # soup = BeautifulSoup(webpage, 'html.parser')
    # info = soup.find_all("td", class_ = "chart-table-track")
    # streams = soup.find_all("td", class_ = "chart-table-streams")

    # i = 0

    # while i < n:
    
    #     song = info[i].find('strong').get_text()
    #     artist = info[i].find('span').get_text()
    #     streamCount = streams[i].get_text()

    #     infos.append({'rank':i+1, 'song':song, 'artist':artist, 'streams':streamCount})

    #     i += 1
    # jsonStr = json.dumps(infos, indent=4)
    # jsonFile = open("dataTop.json", "w")

    with open("dataTop.json", 'r') as j:
                jsonFile = json.loads(j.read())

    # jsonFile.write(jsonStr)
    # jsonFile.close()
    
    # return (infos)
    return (jsonFile)

# billboardCategories()
# categoryLinkToTitle("/charts/streaming-songs")
# tracks = billboardTracks("/charts/billboard-200/", 100)
# print(tracks)
# tracks = billboardTracks("/charts/radio-songs/","")