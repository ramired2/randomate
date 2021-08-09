import requests
from bs4 import BeautifulSoup
# import os
from requests.sessions import Request
from urllib.request import urlopen, Request
import json

def read(country, n):
    URL ="https://www.spotifycharts.com/regional/" + country + "/daily/latest"
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})

    infos = []

    webpage = urlopen(req).read()

    soup = BeautifulSoup(webpage, 'html.parser')
    info = soup.find_all("td", class_ = "chart-table-track")
    streams = soup.find_all("td", class_ = "chart-table-streams")

    i = 0

    while i < n:
    
        song = info[i].find('strong').get_text()
        artist = info[i].find('span').get_text()
        streamCount = streams[i].get_text()

        infos.append({'rank':i+1, 'song':song, 'artist':artist, 'streams':streamCount})

        i += 1
    jsonStr = json.dumps(infos, indent=4)
    jsonFile = open("dataTop.json", "w")
    jsonFile.write(jsonStr)
    jsonFile.close()
    
    return (infos)