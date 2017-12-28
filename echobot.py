import json
from configuration import *
import requests

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
    print (js)

get_information()    
