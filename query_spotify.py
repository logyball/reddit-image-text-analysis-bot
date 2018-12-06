import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from os import environ
import random
CLIENT_ID=environ['SPOTIFY_CLIENT_ID']
CLIENT_SECRET=environ['SPOTIFY_CLIENT_SECRET']

def get_a_playlist(query):
    #This function will return a link to a spotify playlist given query parmaters
    #A random integer is generated to ensure that a different link is given with the same query
    offset = random.randint(1,20)
    credentials = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    spotify = spotipy.Spotify(client_credentials_manager=credentials)
    results = spotify.search(query,limit=1, offset=offset,type='playlist')
    link = results['playlists']['items'][0]['external_urls']['spotify']
    return link


