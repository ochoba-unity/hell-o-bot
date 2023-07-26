from html.parser import HTMLParser
import telebot
import time
import requests
import json

TOKEN = "295118557:AAGM_Dqbm2NCH0El1zXYirAwcAY6BXypA3w"
hello_image = open(file="faq_image.jpg", mode="rb")

rules = ""


def check_users():
    try:
        def return_username(dct):
            return Chatter(username=dct['username'], present=dct['present'])

        read_from = open(file="users.json", mode="r")
        sttt = ""
        for i in read_from.readlines():
            sttt += i.strip("\n")
        return json.loads(sttt, object_hook=return_username)

    except json.decoder.JSONDecodeError or FileNotFoundError:
        file = open(file="users.json", mode="w")
        print("[]", file=file)


def read_users():
    def return_username(dct):
        return Chatter(username=dct['username'], present=dct['present'])

    read_from = open(file="users.json", mode="r")
    sttt = ""
    for i in read_from.readlines():
        sttt += i.strip("\n")
    return json.loads(sttt, object_hook=return_username)


class Chatter:
    username = ""
    present = 1

    def __init__(self, username, present):
        self.username = username
        self.present = present


class ChatterEncoder(json.JSONEncoder):
    def default(self, o):
        return {"username": o.username, "present": o.present}



class MyHTMLParser(HTMLParser):
    def reset(self):
        HTMLParser.reset(self)
        self.data = ''

    def handle_data(self, data):
        self.data += data + ' '


def get_page(url):
    r = requests.get(url)
    if r.status_code == 200:
        page = r.text
    return page


def dump(user_list):
    chatter_list = open(file="users.json", mode="w")
    json.dump(user_list, fp=chatter_list, cls=ChatterEncoder)
    chatter_list.close()

