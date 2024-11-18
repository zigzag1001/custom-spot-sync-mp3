import dotenv
import requests
import json
import base64

URL_AUTH = "https://accounts.spotify.com/authorize"
URL_TOKEN = "https://accounts.spotify.com/api/token"

config = dotenv.dotenv_values()

id_secret = f"{config['SPOTIFY_CLIENT_ID']}:{config['SPOTIFY_CLIENT_SECRET']}"
id_secret_b64 = base64.b64encode(id_secret.encode()).decode()

def update_refresh_token(refresh_token):
    with open(".env", "r+") as f:
        refresh_token_line = f"SPOTIFY_REFRESH_TOKEN = {refresh_token}\n"
        file_text = f.read()
        f.seek(0)
        new_text = ""
        if "SPOTIFY_REFRESH_TOKEN" in file_text:
            file_text = file_text.split("\n")
            for line in file_text:
                if not line.startswith("SPOTIFY_REFRESH_TOKEN"):
                    new_text += line + "\n"
                else:
                    new_text += refresh_token_line
        else:
            new_text = file_text + "\n" + refresh_token_line
        f.write(new_text)
        f.truncate()

def get_first_spot_access_token():


    request_body = {
        "client_id": config["SPOTIFY_CLIENT_ID"],
        "response_type": "code",
        "redirect_uri": config["SPOTIFY_REDIRECT_URI"],
        "scope": "playlist-read-private"
    }

    print("Visit the following URL to get the code:")

    print(URL_AUTH + "?" + "&".join([f"{k}={v}" for k, v in request_body.items()]))

    response = input("Enter the URL you were redirected to: ")

    response = response.split("?")[1].split("&")[0].split("=")

    if response[0] == "code":
        code = response[1]
        print("Code:", code)
    else:
        print("Invalid response")
        raise Exception("Invalid response from Spotify\nYou most likely did not authorize the application")

    request_body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config["SPOTIFY_REDIRECT_URI"],
    }

    headers = {
            'Authorization': f"Basic {id_secret_b64}",
            'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(URL_TOKEN, headers=headers, data=request_body)

    response_dict = json.loads(response.text)

    if "refresh_token" in response_dict:
        update_refresh_token(response_dict["refresh_token"])

    return response_dict

def refresh_spot_access_token(refresh_token):

    request_body = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
    }

    headers = {
            'Authorization': f"Basic {id_secret_b64}",
            'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(URL_TOKEN, headers=headers, data=request_body)

    response_dict = json.loads(response.text)

    if "refresh_token" in response_dict:
        update_refresh_token(response_dict["refresh_token"])

    return response_dict