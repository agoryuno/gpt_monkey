# gpt_monkey

This is a Flask service that creates a local API server for ChatGPT. It's primary purpose is to allow programmatic access to GPT4.

## How it works

It sets up a Flask app that listens for requests containing a prompt message, relays the message to a userscript running in a 
browser tab opened on the 'chat.openai.com' URL. The userscript enters the prompt into the input box of the ChatGPT interface, waits for
the response to be fully generated and sends it back to the Flask app, which relays it back to the caller.

It is left up to the user to open the page in the browser and select the needed GPT model in the dropdown at the top of the page.

## Installation

1. Install Python requirements using:

    pip install -r requirements.txt

2. Generate a `config.ini` file with:

    python config.py

3. Create a new user using the `token_manager.py` script. This is needed in case
the server is exposed to the internet. When creating a user you can provide an integer
ID or one will be created for you:

    python token_manager.py create-user <your_id>

After the user is created, the script will print out a token that you can use to authenticate with the API.


