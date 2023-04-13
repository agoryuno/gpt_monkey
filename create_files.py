import argparse
import sys
import secrets

from utils import get_config

config = get_config('config_template.ini')

HOST = config["MAIN"]["HOST"]
PORT = config["MAIN"]["PORT"]
UPATH = "gptmonkey.user.js"
CPATH = "config.ini"


def generate_flask_secret_key():
    return secrets.token_hex(16)


def make_userscript(token, fpath=UPATH, host=HOST, port=PORT):
    with open("userscript.template", "r") as file:
        content = file.read()

    formatted_string = eval(f"f'''{content}'''")

    with open(fpath, "w") as file:
        file.write(formatted_string)


def make_config_file(fpath=CPATH):
    secret_key = generate_flask_secret_key()
    with open("config_template.ini", "r") as file:
        content = file.read()
    
    formatted_string = eval(f"f'''{content}'''")

    with open(fpath, "w") as file:
        file.write(formatted_string)


def main():
    parser = argparse.ArgumentParser(description="Token Template")
    parser.add_argument("--token", type=str, default=None, help="a valid token (optional)")

    args = parser.parse_args()

    if args.token is None:
        make_config_file()
    else:
        token = args.token
        make_userscript(token)


if __name__ == "__main__":
    main()
