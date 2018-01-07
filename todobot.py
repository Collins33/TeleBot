import json

from configuration import *

import requests

import time

import urllib

from dbhelper import DBHelper

#create instance of the dbhelper
db=DBHelper()

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


def handle_updates(updates):
    #loop through updates and get the result array
    for update in updates["result"]:
        try:
            #get the text
            text=update["message"]["text"]
            #get the chat id
            chat=update["message"]["chat"]["id"]
            #get items from the db
            items=db.get_items(chat)
            if text in items:
                #check if they are duplicates
                db.delete_item(text,chat)
                items=db.get_items(chat)
                keyboard = build_keyboard(items)
                send_message("Select an item to delete", chat, keyboard)
            elif text == "/done":
                keyboard=build_keyboard(items)
                send_message("Select item to delete",chat,keyboard)

            else:
                db.add_item(text,chat)
                items=db.get_items(chat)
                #if it is not a duplicate,add to the db
                items=db.get_items()

               message="\n".join(items)
            #send the message
               send_message(message,chat)
        except KeyError:
            pass


#get the last message sent to the bot
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

#send the last message to the bot
def send_message(text, chat_id,reply_markup=None):
    text=urllib.parse.quote_plus(text)#handle errors of special characters
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    if reply_markup:
        url +="&reply_markup={}".format(reply_markup)
    get_url(url)

#method to add a custom keyboard
def build_keyboard(items):
    #construct the list of items
    keyboard=[[item] for item in items]
    #build a dictionary
    reply_markup={"keyboard":keyboard,"one_time_keyboard":True}#keyboard should appear once user has made a choice
    #convert dictionary into json
    return json.dumps(reply_markup)





#gets the most recent message every 0.5 seconds
def main():
    db.setUp()
    last_update_id=None
    while True:
        updates=get_updates(last_update_id)
        if len(updates["result"])>0:
            last_update_id=get_last_update_id(updates)+1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()


# send_message(text, chat)
