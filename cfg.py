from html.parser import HTMLParser
import telebot
import time
import requests
import json

TOKEN = "295118557:AAGM_Dqbm2NCH0El1zXYirAwcAY6BXypA3w"
hello_image = open(file="faq.jpg", mode="rb")

rules = "Huyavila \n \
Привет, роднуля, ты думаешь я тут от нехуй делать сижу? Проходи.\
1. Представься, расскажи о себе.\
2. Уважай всех участников конфы.\
3. Долго молчишь - вылетаешь. Чуть-чуть молчишь - вылетаешь.\
4. Не ходишь на сходки - получаешь дурную славу.\
5. Тян можешь искать в других конфах, мы тут увожаемые люди.\
Добро пожаловать."


def check_users():
    try:
        read_users()
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
