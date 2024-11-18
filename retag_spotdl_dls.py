import os
import dotenv
import eyed3

eyed3.log.setLevel("ERROR")

# retag song to only have one artist, keep all other metadata

config = dotenv.dotenv_values()

def retag_spotdl_dls(new_files):
    output_path = config.get('OUTPUT_PATH', './mp3/')
    retagged = []
    for file in new_files:
        audiofile = eyed3.load(os.path.join(output_path, file))
        artists = audiofile.tag.artist
        if '/' in artists:
            audiofile.tag.artist = artists.split('/')[0]
            audiofile.tag.save()
            retagged.append(file)

    retagged_str = '\n'.join(retagged)

    print(f"Retagged files:\n{retagged_str}")
