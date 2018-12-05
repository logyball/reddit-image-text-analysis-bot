import giphy_client
from giphy_client.rest import ApiException
import random
import sys
API_KEY = '0VWvIBB8nWFQGmKKv2OIsjajXurXmQGJ'

def query_giphy(query):
    api_instance = giphy_client.DefaultApi()
    off = random.randint(0,50)
    try:
        api_response = api_instance.gifs_search_get(API_KEY, query, limit=1, offset=off, rating='g', lang='en', fmt='json')
        return api_response.data[0].embed_url
    except ApiException as e:
        return None

