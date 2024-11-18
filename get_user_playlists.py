import requests
import json


IGNORE_PLAYLISTS = ['Discover Weekly', "Новый год"]

def get_user_playlists(headers):

    URL_PLAYLISTS = 'https://api.spotify.com/v1/me/playlists'

    next = True

    playlists = {}

    while next:
        response = requests.get(URL_PLAYLISTS, headers=headers)
        response_dict = json.loads(response.text)
        playlists.update({item['name']: item for item in response_dict['items'] if item['name'] not in IGNORE_PLAYLISTS})
        if response_dict['next']:
            URL_PLAYLISTS = response_dict['next']
        else:
            next = False

    return playlists
