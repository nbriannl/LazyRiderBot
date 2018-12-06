import json # to parse json responses into python dictionaries
import requests # to make web requests using Python and interact with python
import time 
import urllib
from datetime import datetime

# Global variables
TOKEN = "670223024:AAEJhUUI2FJ2WjQru1PkydmXLqbfPGUhNDs"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

# Helper function for get_json_from_url
# Params: URL
# Returns: JSON content as string
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")  # .decode("utf8") for extra compatibility
    return content

# Params: URL
# Returns: JSON content as dictionary 
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

# Calls getUpdates API
# Returns: JSON content as dictionary
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100" #long polling at 100s
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

# Params: JSON content of Updates
# Returns: The max values of all updates_id 
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]: #See: https://core.telegram.org/bots/api#making-requests
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat_id = update["message"]["chat"]["id"]
            send_message(text, chat_id)
        except Exception as e:
            print(e)

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    
def main():
    last_update_id = None
    while True:
        print("[{}]".format(datetime.now().time()) , "Getting updates. last_update_id:", last_update_id)
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)

# If `python echo.py` is run on command line, this will run
# See: https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__':
    main()