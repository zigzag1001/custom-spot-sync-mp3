import subprocess


MUSIC_PATH = "./music"

def do_rsgain():
    command = ['rsgain', 'easy', '-p', 'no_album', '-S', MUSIC_PATH]
    subprocess.run(command, check=True)

