import os
import dotenv
import eyed3

eyed3.log.setLevel("ERROR")

config = dotenv.dotenv_values()

possible_hq_files = [".mp3", ".flac", ".wav"]

OUTPUT_PATH = "./music/"

IGNORE_ARTISTS = ["Turbo"]

# if file is mp3 and bitrate is 320kbps add to 320.m3u8
# if file is flac or wav add to 320.m3u8

def get_bitrate(file):
    audiofile = eyed3.load(file)
    return audiofile.info.bit_rate_str if audiofile else None

def walk_dir(dir):
    hqs = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(tuple(possible_hq_files)):
                if any(file.startswith(artist) for artist in IGNORE_ARTISTS):
                    continue
                file_path = os.path.join(root, file)
                bitrate = get_bitrate(file_path)
                trimmed_path = file_path.replace(OUTPUT_PATH, "")
                if bitrate and "320" in bitrate:
                    hqs.append(trimmed_path)
                elif file.endswith((".flac", ".wav")):
                    hqs.append(trimmed_path)
    return hqs

def update_m3u8(file, hqs):
    with open(file, "w") as f:
        for hq in hqs:
            f.write(hq + "\n")

def main():
    hqs = walk_dir(OUTPUT_PATH)
    m3u8_path = os.path.join(OUTPUT_PATH, "320.m3u8")
    update_m3u8(m3u8_path, hqs)
    print(f"HQs: {len(hqs)}")
