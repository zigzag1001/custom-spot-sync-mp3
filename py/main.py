import get_spot_access_token
import get_user_playlists
import download_spot_playlists
import retag_spotdl_dls
import del_m3u
# import hq_320_m3u8
import get_dupes
import do_rsgain
import ntfy

import dotenv

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

    if len(new_files) > 0:
        title = "Spotify Synced"
        message = f"{len(new_files)} new songs downloaded!\n"

        if len(new_files) < 10:
            for file in new_files:
                message += f" - {file}\n"

        ntfy.send_ntfy_notification(title, message)

    retag_spotdl_dls.retag_spotdl_dls(new_files)

    do_rsgain.do_rsgain()

    # Not needed since i found out about Navidrome Smart Playlists
    # hq_320_m3u8.main()

    get_dupes.get_dupes()

    del_m3u.delete_del_m3u()


try:
    main()
except Exception as e:
    print(e)

    title = "EXCEPTION in Spotify Sync"
    message = f"{e}"

    ntfy.send_ntfy_notification(title, message)

