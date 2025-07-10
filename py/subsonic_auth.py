# get subsonic auth headers with navidrome user + pass + salt
#
# token = md5(pass+salt)

import dotenv
import hashlib

def get_subsonic_auth_headers():
    """
    Returns the headers needed for Subsonic authentication.
    """
    config = dotenv.dotenv_values()

    user = config["NAVI_USER"]
    passwd = config["NAVI_PASS"]
    salt = config["SALT"]
    version = config["SUB_VER"]
    c = config["SUB_C"]

    token = hashlib.md5((passwd + salt).encode('utf-8')).hexdigest()

    # ret = f"u={user}&t={token}&v={version}&c={c}"
    ret = {
        "u": user,
        "t": token,
        "s": salt,
        "v": version,
        "c": c,
        "f": "json"
    }

    return ret
