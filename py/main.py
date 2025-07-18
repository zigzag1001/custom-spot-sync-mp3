import get_spot_access_token
import get_user_playlists
import download_spot_playlists
import retag_spotdl_dls
import del_m3u
# import hq_320_m3u8
import get_dupes
import dotenv
import requests

OUTPUT_PATH = "./music/"
def main():
    with open(".env", "r") as f:
        if "SPOTIFY_REFRESH_TOKEN" not in f.read():
            get_spot_access_token.get_first_spot_access_token()


    config = dotenv.dotenv_values()

    access_token = get_spot_access_token.refresh_spot_access_token(config["SPOTIFY_REFRESH_TOKEN"])['access_token']

    headers = {
            "Authorization": f"Bearer {access_token}",
    }

    playlists = get_user_playlists.get_user_playlists(headers)

    new_files = download_spot_playlists.download_spot_playlists(playlists)

    if config.get("NTFY_url") != None and len(new_files) > 0:
        ntfy_url = config["NTFY_url"]
        ntfy_user = config.get("NTFY_USER")
        ntfy_password = config.get("NTFY_PASSWORD")

        if ntfy_user and ntfy_password:
            auth = (ntfy_user, ntfy_password)
        else:
            auth = None
        headers = {
            "t": "Spotify Synced"
        }
        data = f"{len(new_files)} new songs downloaded!"
        
        response = requests.post(ntfy_url, headers=headers, data=data, auth=auth)

    retag_spotdl_dls.retag_spotdl_dls(new_files)

    # Not needed since i found out about Navidrome Smart Playlists
    # hq_320_m3u8.main()

    get_dupes.get_dupes()

    del_m3u.delete_del_m3u()


try:
    main()
except Exception as e:
    print(e)
    config = dotenv.dotenv_values()

    ntfy_url = config["NTFY_url"]

    ntfy_user = config.get("NTFY_USER")
    ntfy_password = config.get("NTFY_PASSWORD")

    if ntfy_user and ntfy_password:
        auth = (ntfy_user, ntfy_password)
    else:
        auth = None

    headers = {
        "t": "EXCEPTION in Spotyify Sync"
    }

    data = f"{e}"

    response = requests.post(ntfy_url, headers=headers, data=data, auth=auth)

    print(response.status_code)
