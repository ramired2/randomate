import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from bs4 import BeautifulSoup
import pprint
import spotipy.util as util
from urllib.request import urlopen, Request
import json

def processSearch(word, size):
    username = 'rand'
    SPOTIPY_CLIENT_ID='819d96e619f64cb28685ed00e6f09761'
    SPOTIPY_CLIENT_SECRET='21c263b89ced4297b52fcc70d76b99fe'
    SPOTIPY_REDIRECT_URI='https://www.colorhexa.com/'
    SCOPE = 'user-read-private'

    token = util.prompt_for_user_token(username=username, scope=SCOPE, 
                                   client_id=SPOTIPY_CLIENT_ID,   
                                   client_secret=SPOTIPY_CLIENT_SECRET,     
                                   redirect_uri=SPOTIPY_REDIRECT_URI)


    searching(word, size, token)

# uses token to find n amount of playlists
def searching(word, n, toke):
    headers = {'Authorization': 'Bearer ' + toke,}

    params = (('query', word), ('type', 'playlist'), ('market', 'US'), ('offset', '0'), ('limit', n),)

    response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
    response.raise_for_status()


    jsonInfo = response.json()
    jsonInfo = jsonInfo['playlists']
    jsonInfo = jsonInfo["items"]

    writeFile(jsonInfo)

    return jsonInfo

def writeFile (jsonInfo):
    jsonString = json.dumps(jsonInfo, indent=4)
    jsonFile = open("dataSearch.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

def getTracks(playlistId, creatorId):
    # request tom's microservice, for now json file w specific info
    URL = "http://flip1.engr.oregonstate.edu:8000/playlist?playlistId="+playlistId
    # will be used
    #input the playlist id in the link
    # receive = requests.get('URL UNKNOWN YET')
    # req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    
    response = requests.get(URL)
    # print(response.json())
    jsonInfo = response.json()


    playlistName = jsonInfo["name"]
    # print(playlistName)

    jsonInfo = jsonInfo["tracks"]
    length = len(jsonInfo["items"])
    # jsonInfo = jsonInfo["items"][0]["track"]
    # print(jsonInfo)

    oof = []

    i = 0

    while i < length:
        cut = jsonInfo["items"][i]["track"]

        # print(len(cut))
        # print(type(cut))
        # print(cut.keys())
        artist = jsonInfo["items"][i]["track"]["artists"][0]["name"]
        id = jsonInfo["items"][i]["track"]["artists"][0]["id"]
        # data[0]['artistName'] = artist
        cut["artistName"] = artist
        cut["artistId"] = id
        # print(artist)
        # print(cut)
        oof.append(cut)
        # oof[i].insert({"artistName":artist, "artistId":id})
        
        i+=1

    # print(oof)
    # print(type(oof))

    jsonStr = json.dumps(oof, indent=4)
    jsonFile = open("dataTracks.json", "w")
    jsonFile.write(jsonStr)
    jsonFile.close()

    return playlistName