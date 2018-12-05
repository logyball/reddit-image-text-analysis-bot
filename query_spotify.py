import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from os import environ
import random
CLIENT_ID = 'd3d39178dcd344c1b1eb1933447ecffd'
CLIENT_SECRET = 'de9d83475e2b4f3897e8be424d26a6f7'
#client_id=environ[CLIENT_ID]
#client_secret=environ[CLIENT_SECRET]

def get_a_playlist(query):
    #This function will return a link to a spotify playlist given query parmaters
    #A random integer is generated to ensure that a different link is given with the same query
    offset = random.randint(1,20)
    credentials = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    spotify = spotipy.Spotify(client_credentials_manager=credentials)
    results = spotify.search(query,limit=1, offset=offset,type='playlist')
    link = results['playlists']['items'][0]['external_urls']['spotify']
    return link

print(get_a_playlist('nervous'))
