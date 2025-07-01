import dotenv
import subsonic_auth
import requests
import json

config = dotenv.dotenv_values()

url = config["NAVI_URL"]
if not url.endswith('/'):
    url += '/'
if not url.startswith('http'):
    url = 'http://' + url
params = subsonic_auth.get_subsonic_auth_headers()

def do_request(endpoint, params):
    response = requests.get(url + endpoint, params=params)
    return response.json()

def get_playlists():
    ep = "/rest/getPlaylists"
    response = do_request(ep, params)
    ret = response.get("subsonic-response", {})
    return ret.get("playlists", {}).get("playlist", [])

#             "playlist": [
#                 {
#                     "id": "1dfce8ea-1528-46b2-9e80-953cc44872c1",

def get_playlist(playlist_id):
    ep = "/rest/getPlaylist"
    response = do_request(ep, {**params, "id": playlist_id})
    ret = response.get("subsonic-response", {})
    return ret.get("playlist", {})


def main():
    # Example usage
    playlists = get_playlists()
    # print(json.dumps(playlists, indent=2))
    pl = playlists[0]["id"]
    p = get_playlist(pl)
    print(json.dumps(p, indent=4))

if __name__ == "__main__":
    main()
