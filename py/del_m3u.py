





import os
import dotenv

config = dotenv.dotenv_values()

OUTPUT_PATH = "./music/"

def delete_del_m3u():
    music = os.listdir(OUTPUT_PATH)

    initlen = len(music)

    if "del.m3u" in music:
        with open(f"{OUTPUT_PATH}del.m3u", "r") as f:
            lines = f.readlines()
        if lines == []:
            return 0
        todelete = []
        print("To Delete:")
        for line in lines:
            if line.startswith("#"):
                continue
            line = line.strip()
            tmp_line = "/".join(line.split("/")[2:])
            todelete.append(tmp_line)
            print(f"{OUTPUT_PATH}{tmp_line}")

        for item in todelete:
            try:
                os.remove(f"{OUTPUT_PATH}{item}")
            except Exception as e:
                print(item, "failed deletion", e)
        try:
            os.remove(f"{OUTPUT_PATH}del.m3u")
        except Exception as e:
            print("del.m3u", "failed deletion", e)
    print(f"{initlen - len(os.listdir(OUTPUT_PATH))} Songs Removed")
