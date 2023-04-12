// ==UserScript==
// @name         ChatGPT browser interface
// @namespace    https://github.com/agoryuno/gpt4_monkey
// @version      0.0.1
// @description  Allows programmatic access to ChatGPT in the browser
// @author       Alex Goryunov
// @match        https://chat.openai.com/*
// @grant        none
// @updateURL    https://github.com/agoryuno/gpt_monkey/raw/master/userscript.user.js
// @downloadURL  https://github.com/agoryuno/gpt_monkey/raw/master/userscript.user.js
// @require      http://127.0.0.1:6758/resources/js/socket.io.js
// @require      https://cdn.jsdelivr.net/npm/@violentmonkey/dom@2
// ==/UserScript==

// Locally hosted socket.io.js libary is needed due to a Firefox bug
// that prevents properly loading mapping files in userscripts

(function() {
  'use strict';

  // This is needed to prevent iframes from
  // opening extra connections
  if (window !== top) {
    return
  };

  // Constants
  const HOST = 'ws://127.0.0.1';
  const PORT = 6758;
  const TOKEN = '';

  // Create WebSocket URL with token parameter
  const webSocketURL = `${HOST}:${PORT}?token=${encodeURIComponent(TOKEN)}`;

  // Create WebSocket connection
  const socket = io(webSocketURL);

  socket.on('connect', () => {
    console.log('WebSocket connection opened');
  });

  socket.on('disconnect', (reason) => {
    console.log('WebSocket connection closed:', reason);
  });

  socket.on('message', (...args) => {
    set_input_value(args[0]);
    console.log('Message received:', args[0]);
    track_generation();
  });


  // Connection error
  socket.addEventListener('error', (event) => {
      console.error('WebSocket encountered an error:', event);
  });


  const get_input_box = () => {
    const textarea = document.querySelector('main form textarea');
    if (textarea) {
      return textarea;
    }
    return false;
  }

  const get_input_div = () => {
    const idiv = document.querySelector('main div>form>div');
    if (idiv) {
      return idiv;
    }
    return false;
  }

  const set_input_value = (txt) => {
    const inp_box = get_input_box();
    if (inp_box) {
      inp_box.value = txt;
      trigger_send_click(inp_box);
    }
  }

  // Helper function to trigger a click event on the "Send" button
const trigger_send_click = (inp_box) => {
  if (inp_box) {
    const send_button = inp_box.nextElementSibling;
    if (send_button) {
      send_button.click();
    }
  }
}


  let chat_history = null;

  const get_chat_element = VM.observe(document.body,
                             () => {
    const chat_element = document.querySelector('main>div>div>div>div');

    if (chat_element) {
      chat_history = chat_element;
      return true;
    }

  });

const track_generation = () => {
  const input_div = get_input_div();

  if (input_div) {
    VM.observe(input_div, (mutations, observer) => {
      for (let mutation of mutations) {
        if (mutation.removedNodes.length == 1) {
          let node = mutation.removedNodes[0];
          if (node.tagName.toLowerCase() === 'button' &&
              node.innerText == "Stop generating") {
              //console.log(node);
              const hist = Array.from(chat_history.querySelectorAll("div.group"));
              socket.emit("message", hist[hist.length-1].innerText);
          }
        }
      }
    });
  }
}


})();