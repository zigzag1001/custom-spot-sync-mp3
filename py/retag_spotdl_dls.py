import os
import eyed3
from mutagen.oggopus import OggOpus

eyed3.log.setLevel("ERROR")

OUTPUT_PATH = "./music/"

# retag song to only have one artist, keep all other metadata

def retag_spotdl_dls(new_files):
    retagged = []
    for file in new_files:
        path = os.path.join(OUTPUT_PATH, file)

        if file.endswith(".mp3"):
            audiofile = eyed3.load(path)
            if not audiofile or not audiofile.tag or not audiofile.tag.artist:
                print(f"Skipping {file}, no artist tag found.")
                continue
            artists = audiofile.tag.artist
            if '/' in artists:
                audiofile.tag.artist = artists.split('/')[0]
                audiofile.tag.save()
                retagged.append(file)

        elif file.endswith(".opus"):
            audiofile = OggOpus(path)
            artists = audiofile.get("artist", [None])
            if not artists:
                print(f"Skipping {file}, no artist tag found.")
                continue
            if len(artists) > 1:
                audiofile["artist"] = artists[0]
                audiofile.save()
                retagged.append(file)

    print("Retagged files:\n" + "\n".join(retagged))
