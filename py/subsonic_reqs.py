import dotenv
import subsonic_auth
import ntfy
import requests
import json
import os
import re

config = dotenv.dotenv_values()

url = config["NAVI_URL"]
# music_dir = config["MUSIC_DIR"]
# music_dir = "/app/music"
music_dir = "/app/"
print(f"Using music directory: {music_dir}")
if not url.endswith('/'):
    url += '/'
if not url.startswith('http'):
    url = 'http://' + url
params = subsonic_auth.get_subsonic_auth_headers()

def do_request(endpoint, params):
    response = requests.get(url + endpoint, params=params)
    if response.status_code != 200:
        print(f"Request Error: {response.status_code} - {response.text}")
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

def rm_pl_song(pl_id, song_idx):
    ep = "/rest/updatePlaylist"
    response = do_request(ep, {**params, "playlistId": pl_id, "songIndexToRemove": song_idx})
    return response

def get_song(id):
    ep = "/rest/getSong"
    response = do_request(ep, {**params, "id": id})
    ret = response.get("subsonic-response", {})
    return ret.get("song", {})


def main():
    # Example usage
    # playlists = get_playlists()
    # print(json.dumps(playlists, indent=2))
    #
    # pl = playlists[0]["id"]
    # p = get_playlist(pl)
    # print(json.dumps(p, indent=4))
    #
    # id = "05db0720878054423aefa3bf91b4b206"
    # song = get_song(id)
    # print(json.dumps(song, indent=4))
    
    # get playlist with name "del" -> get all song paths -> rm them
    playlists = get_playlists()
    for playlist in playlists:
        if playlist["name"] == "del":

            pl = get_playlist(playlist["id"])
            delete_count = 0
            fail_count = 0

            for song in pl.get("entry", []):

                song_path = song.get("path", "")
                full_path = os.path.join(music_dir, "." + song_path)

                if os.path.exists(full_path):
                    response = rm_pl_song(playlist["id"], 0)
                    print(response)
                    os.remove(full_path)
                    print(f"Deleted: {full_path}")
                    delete_count += 1

                else:
                    print(f"File not found: '{full_path}'")
                    fail_count += 1
                    # print(os.listdir(music_dir))

            if delete_count > 0:
                title = "Deleted Songs"
                message = f"Deleted {delete_count} songs"
                if fail_count > 0:
                    message += f", failed to delete {fail_count} songs."
                ntfy.send_ntfy_notification(title, message)

        elif playlist["name"] == "spoticheck":

            if playlist["songCount"] > 0:

                pl = get_playlist(playlist["id"])

                for song in pl.get("entry", []):
                    response = rm_pl_song(playlist["id"], 0)
                    print(response)
                # run main spotify sync
                print("Running Spotify sync...")
                import main
                main.main()

        elif re.match(r"open\.spotify\.com\/track\/", playlist["name"]):
            if playlist["songCount"] > 0:
                pl = get_playlist(playlist["id"])
                for song in pl.get("entry", []):
                    response = rm_pl_song(playlist["id"], 0)
                    print(response)
                # run spotdl
                print("spotdl not implemented yet")


if __name__ == "__main__":
    main()
