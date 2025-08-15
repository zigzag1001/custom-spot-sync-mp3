import requests
import dotenv

def send_ntfy_notification(title, message):
    config = dotenv.dotenv_values()

    ntfy_url = config["NTFY_url"]

    ntfy_user = config.get("NTFY_USER")
    ntfy_password = config.get("NTFY_PASSWORD")

    if ntfy_user and ntfy_password:
        auth = (ntfy_user, ntfy_password)
    else:
        auth = None

    headers = {
        "t": title
    }

    data = message

    response = requests.post(ntfy_url, headers=headers, data=data, auth=auth)

    return response
