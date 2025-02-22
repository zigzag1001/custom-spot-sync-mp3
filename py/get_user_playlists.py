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
        if "items" not in response_dict:
            print(response_dict)
            raise Exception(f"NO ITEMS IN RESPONSE: {response_dict}")

        items_copy = response_dict["items"].copy()
        response_dict["items"] = [i for i in items_copy if i is not None]

        playlists.update({item.get('name'): item for item in response_dict['items'] if item.get('name') not in IGNORE_PLAYLISTS})
        if response_dict['next']:
            URL_PLAYLISTS = response_dict['next']
        else:
            next = False

    return playlists
