import get_spot_access_token
import get_user_playlists
import download_spot_playlists
import retag_spotdl_dls
import hq_320_m3u8
import get_dupes
import dotenv

OUTPUT_PATH = "./music/"

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

retag_spotdl_dls.retag_spotdl_dls(new_files)

hq_320_m3u8.main()

get_dupes.get_dupes()
