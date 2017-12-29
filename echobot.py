import json
from configuration import *
import requests
import time

URL="https://api.telegram.org/bot{}/".format(TelegramToken)#url to build the request

#make a request to telegram using the created url
def get_url(url):
    response=requests.get(url)
    content= response.content.decode("utf8")
    return content

#parse the result into python dictionary
def get_json_url(url):
    content=get_url(url)
    js=json.loads(content)
    return js

#get information about the bot
def get_information():
    url=URL+"getme"
    js=get_json_url(url)
    return js

#get messages sent to the bot
def get_updates(offset=None):
    url=URL+"getUpdates"
    if offset:
        url +="?offset={}".format(offset)
    js=get_json_url(url)
    return js

#function that calculates the highest id of the updates we receive from get_updates
def get_last_update_id(updates):
    update_ids=[]
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    #return the max id which is the most recent
    return max(update_ids)


#function to send an echo reply for each message we receive
def echo_all(updates):
    for update in updates["result"]:
        try:
            text=update["message"]["text"]
            chat=update["message"]["chat"]["id"]
            send_message(text,chat)
        except Exception as e:
            print(e)

#get the last message sent to the bot
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

#send the last message to the bot
def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

#gets the most recent message every 0.5 seconds
def main():
    last_update_id=None
    while True:
        updates=get_updates(last_update_id)
        if len(updates["result"])>0:
            last_update_id=get_last_update_id(updates)+1
            echo_all(updates)
        time.sleep(0.5)    


if __name__ == '__main__':
    main()








# send_message(text, chat)
