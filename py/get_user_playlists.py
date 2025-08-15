import requests
import json
import os


# IGNORE_PLAYLISTS = ['Discover Weekly', "Новый год"]
spotify_playlists_json = "spotify_playlists.json"

# Case sensitive name or url of the playlist
def get_w_b_lists(file):
    if not os.path.exists(file):
        return {}
    with open(file, 'r', encoding='utf-8') as f:
        lists = json.load(f)

    whitelist = lists.get('whitelist', [])
    blacklist = lists.get('blacklist', [])

    if len(whitelist) > 0 and len(blacklist) > 0:
        print("Both whitelist and blacklist are defined. Using whitelist only.")
        return {"status": "w", "whitelist": whitelist, "blacklist": []}
    elif len(whitelist) > 0:
        return {"status": "w", "whitelist": whitelist, "blacklist": []}
    elif len(blacklist) > 0:
        return {"status": "b", "whitelist": [], "blacklist": blacklist}
    else:
        return {"status": "b", "whitelist": [], "blacklist": []}




def get_user_playlists(headers):

    URL_PLAYLISTS = 'https://api.spotify.com/v1/me/playlists'

    next = True

    playlists = {}

    w_b_lists = get_w_b_lists(spotify_playlists_json)
    if w_b_lists['status'] == 'w':
        print(f"Using whitelist: {w_b_lists['whitelist']}")
    else:
        print(f"Using blacklist: {w_b_lists['blacklist']}")

    while next:
        response = requests.get(URL_PLAYLISTS, headers=headers)
        response_dict = json.loads(response.text)
        if "items" not in response_dict:
            print(response_dict)
            raise Exception(f"NO ITEMS IN RESPONSE: {response_dict}")

        items_copy = response_dict["items"].copy()
        response_dict["items"] = [i for i in items_copy if i is not None]

        # Whitelist/blacklist filtering
        if w_b_lists['status'] == 'w':
            for item in response_dict['items']:
                name = item.get('name')
                url = item.get('external_urls', {}).get('spotify', '')
                if name in w_b_lists['whitelist'] or url in w_b_lists['whitelist']:
                    playlists.update({name: item})
        elif w_b_lists['status'] == 'b':
            for item in response_dict['items']:
                name = item.get('name')
                url = item.get('external_urls', {}).get('spotify', '')
                if name not in w_b_lists['blacklist'] and url not in w_b_lists['blacklist']:
                    playlists.update({name: item})
        else:
            raise Exception(f"???? Unknown status in whitelist/blacklist: {w_b_lists['status']}")

        if response_dict['next']:
            URL_PLAYLISTS = response_dict['next']
        else:
            next = False

    return playlists
