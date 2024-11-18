import subprocess
import dotenv
import os

config = dotenv.dotenv_values()

OUTPUT_PATH = "./music/"

def download_spot_playlists(playlists):

    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    dir_state = os.listdir(OUTPUT_PATH)


    playlist_urls = [playlists[playlist]['external_urls']['spotify'] for playlist in playlists]

    command = ['spotdl', 'download'] + playlist_urls + ['--m3u']

    subprocess.run(command, cwd=OUTPUT_PATH)


    new_state = os.listdir(OUTPUT_PATH)

    new_files = [f for f in new_state if f not in dir_state]

    new_files_str = '\n'.join(new_files)

    print(f"New files:\n{new_files_str}")


    # reverse playlist order

    m3us = [f for f in os.listdir(OUTPUT_PATH) if f.endswith('.m3u8')]

    for m3u in m3us:
        with open(os.path.join(OUTPUT_PATH, m3u), 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            f.writelines(reversed(lines))
            f.truncate()

    return new_files
