import os
import dotenv
import eyed3

eyed3.log.setLevel("ERROR")

config = dotenv.dotenv_values()

def get_dupes():
    output_path = config["OUTPUT_PATH"]
    dupes = []

    allowed_extensions = [".mp3"]

    files = os.listdir(output_path)

    files = [f for f in files if any(f.endswith(ext) for ext in allowed_extensions)]

    artists = {}

    for f in files:
        audiofile = eyed3.load(output_path + f)
        if not audiofile:
            continue
        if audiofile.tag is not None:
            artist = audiofile.tag.artist
            title = audiofile.tag.title
            if artist is None or title is None or "(slowed)" in title:
                continue
            if "(" in title and title.endswith(")"):
                title = title.split("(")[0].strip()
            if artist is not None and title is not None:
                if artist not in artists:
                    artists[artist] = {}
                if title not in artists[artist]:
                    artists[artist][title] = []
                artists[artist][title].append(f)


    # get oldest file
    for artist in artists:
        for title in artists[artist]:
            files = artists[artist][title]
            if len(files) > 1:
                files.sort(key=lambda x: os.path.getmtime(output_path + x), reverse=True)
                for f in files[1:]:
                    dupes.append(f)

    dupes_str = "\n".join(dupes)

    print(f"Duplicates:\n{dupes_str}")

    return dupes
