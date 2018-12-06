import giphy_client
from giphy_client.rest import ApiException
import random
import sys
import os
API_KEY = environ['GIPHY_KEY']


def query_giphy(query):
    """
    Sends a query to the giphy api to get a random GIPH based on the query paramaters.
    """
    api_instance = giphy_client.DefaultApi()
    off = random.randint(0,50)
    try:
        api_response = api_instance.gifs_search_get(API_KEY, query, limit=1, offset=off, rating='g', lang='en', fmt='json')
        return api_response.data[0].embed_url
    except ApiException as e:
        return None

