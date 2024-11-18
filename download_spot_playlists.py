import subprocess
import dotenv
import os

config = dotenv.dotenv_values()

def download_spot_playlists(playlists):

    output_path = config.get('OUTPUT_PATH', './mp3/')

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    dir_state = os.listdir(output_path)


    playlist_urls = [playlists[playlist]['external_urls']['spotify'] for playlist in playlists]
    # playlist_urls = ['https://open.spotify.com/playlist/22hMEOEso4FH9aWfzka5aZ']

    command = ['spotdl', 'download'] + playlist_urls + ['--m3u']

    subprocess.run(command, cwd=output_path)


    new_state = os.listdir(output_path)

    new_files = [f for f in new_state if f not in dir_state]

    new_files_str = '\n'.join(new_files)

    print(f"New files:\n{new_files_str}")


    # reverse playlist order

    m3us = [f for f in os.listdir(output_path) if f.endswith('.m3u8')]

    for m3u in m3us:
        with open(os.path.join(output_path, m3u), 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            f.writelines(reversed(lines))
            f.truncate()

    return new_files
