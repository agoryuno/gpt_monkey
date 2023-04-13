import requests

token = None
host = "127.0.0.1"
port = 6758

def send(message: str) -> str:
    assert token is not None, "Token is not set."
    url = f"http://{host}:{port}/gpt/send_message"
    data = {"token": token, "message": message}

    response = requests.post(url, json=data)

    response.raise_for_status()

    return response.text

