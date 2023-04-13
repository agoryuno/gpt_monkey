# gpt_monkey

This is a Flask service that creates a local API server for ChatGPT. Its' primary purpose is to allow programmatic access to GPT4.

It doesn't require an OpenAI API key, but since GPT4 in ChatGPT is available only to
ChatGPT Plus users - you'll need to be subscribed to that service to use the latest model.
GPT3.5 can be used without a subscription, of course.

## How it works

It sets up a Flask app that listens for requests containing a prompt message and relays the message to a userscript running in a 
browser tab opened on the 'chat.openai.com' URL. The userscript enters the prompt into the input box of the ChatGPT interface, waits for
the response to be fully generated and sends it back to the Flask app, which relays it back to the caller.

It is left up to the user to open the page in the browser and select the needed GPT model in the dropdown at the top of the page.

## Installation

Before installing make sure that you have Python 3.8+ installed. You can check your version by running `python --version`.

### Quick and easy installation

If your OS supports it (e.g., it is not Windows), you can run the `install.sh` script 
which will create all the necessary files. In this case you can skip the next section.

### Manual installation

1. Install Python requirements using:

```
pip install -r requirements.txt
```

2. Generate a `config.ini` file with:

```
python create_files.py
```

3. Create a new user using the `token_manager.py` script. This is needed in case
the server is exposed to the internet. When creating a user you can provide an integer
ID or one will be created for you:

```
python token_manager.py create-user <your_id>
```

Note the user ID that the script returns or use your own for the next step.

4. Create the userscript file. This is a JavaScript file that will be injected into the browser tab.

```
python create_userscript.py <your_user_id>
```

## Installing the userscript

The userscript `gptmonkey.user.js`, that was created for you during the installation, is
located in the project's root directory. You need to install it in your browser.

To do this you need to install a userscript manager. There are several options, but this
service was tested with the open source ViolentMonkey extension:

* [Chrome](https://chrome.google.com/webstore/detail/violentmonkey/jinjaccalgkegednnccohejagnlnfdag)
* [Firefox](https://addons.mozilla.org/en-US/firefox/addon/violentmonkey/)

The exact procedure for installing the userscript depends on the userscript extension you chose.

For ViolentMonkey, you need to click on the monkey icon in the browser toolbar and then
the large + button in the top right corner. You can then copy the contents of the `gptmonkey.user.js` file and use it to replace all of the content in the script editor. 
Save and close the tab with the script editor.

You are done.

## Running the server

To run the server issue the following command from the project's root directory:

```
python app.py
```

Note, that in order for the service to work, you need to have the browser tab with the ChatGPT interface open.

## Testing the service

To make sure everything is working you can use a cURL command to send a request to the server. Replace `<your_token>` with the token that you can find on line 28 of the
`gptmonkey.user.js` file.

Alternatively you can use the `token_manager.py` script to find your token. First find
your user ID by running:

```
python token_manager.py list-users
```

Copy your user ID (there should be only one user) and then run:

```
python token_manager.py list-tokens <your_user_id>
```

Copy the first token and substitute it for `<your_token>` in the cURL command below:

```
curl '127.0.0.1:6758/gpt/send_message' -d 'token=<your_token>' -d 'message="Write%20me%20a%20poem"'
```

Once the command is executed you should see the response after a short delay. You can
also watch the browser tab to see the prompt being entered and the response being generated.

## Using from Python

A small Python package is provided to make using the services a little easier. It is automatically installed as part of the requirements.
To use it:

```python
import gpt_monkey

gpt_monkey.token = "your_token"

gpt_monkey.send("Write me a poem.")
```
    
If you run the service on a host or port that are different from the default, you'll need to set them with:

```python
gpt_monkey.host = "your_host"
gpt_monkey.port = your_port
```
    

