import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
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