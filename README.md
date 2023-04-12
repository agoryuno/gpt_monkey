# gpt_monkey

This is a Flask service that creates a local API server for ChatGPT. It's primary purpose is to allow programmatic access to GPT4.

## How it works

It sets up a Flask app that listens for requests containing a prompt message, relays the message to a userscript running in a 
browser tab opened on the 'chat.openai.com' URL. The userscript enters the prompt into the input box of the ChatGPT interface, waits for
the response to be fully generated and sends it back to the Flask app, which relays it back to the caller.

It is left up to the user to open the page in the browser and select the needed GPT model in the dropdown at the top of the page.
