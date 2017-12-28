import json
from configuration import *
import requests

URL="https://api.telegram.org/bot{}/getme".format(TelegramToken)#url to build the request

def get_url(url):
    response=requests.get(url)
    content= response.content.decode("utf8")
    print (content)

get_url(URL)
