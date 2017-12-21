from datetime import date

from peewee import *
from html.parser import HTMLParser
from random import randint
import peewee
import requests
import telebot
import time

db = SqliteDatabase("database.sqlite")
TOKEN = "295118557:AAFBcBNtPpkVCdiXgeUzPeN2bUzLEEHDkmI"
hello_image = open(file="faq.jpg", mode="rb")

rules = "*Pravila* \n \
Привет, роднуля, ты думаешь я тут от нехуй делать сижу? Проходи.\
1. Представься, расскажи о себе.\
2. Уважай всех участников конфы.\
3. Долго молчишь - вылетаешь. Чуть-чуть молчишь - вылетаешь.\
4. Не ходишь на сходки - получаешь дурную славу.\
5. Еда богов - Парк кур. Напиток богов - кофе.\
6. Тян можешь искать в других конфах, мы тут увожаемые люди.\
7. Томмэ НЕ хороший. \
Добро пожаловать."


class Chatter(Model):
    username = CharField(unique=True)
    stat = IntegerField()
    in_chat = BooleanField(default=True)

    class Meta:
        database = db


class GayDates(Model):
    date = DateField(unique=True)
    gay_name = CharField()
    status = TextField()
    class Meta:
        database = db


class StringHolder(Model):
    key = TextField()
    value = TextField()

    class Meta:
        database = db


lucky_names = ["2d", "Гей", "Миниханчик", "Кира", "Беткоен", "Нефаз", "Мем кек",
               "Сочник"]
actions = ["Шекочу анус @pbsphp", "А Томмэ хороший?", "Шли бы делом занялись, а не рулетки крутили",
           "Треплю @shit_x за щёчку"]

try:
    db.create_table(Chatter)
except peewee.OperationalError:
    pass
try:
    db.create_table(GayDates)
except peewee.OperationalError:
    pass
# I was writing this at 2017.11.19
# GayDates.create(date=date(2017, 11, 19), gay_name="TommyFountaine")
