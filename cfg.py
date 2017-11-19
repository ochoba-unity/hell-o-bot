from datetime import date

from peewee import *
from html.parser import HTMLParser
from random import randint
import peewee
import requests
import telebot
import time

db = SqliteDatabase("database.sqlite")
TOKEN = "295118557:AAGRG0AnxcHndyMIJVCxcWBioXMcgBFnoaU"
hello_image = open(file="faq.jpg", mode="rb")

rules = "Pravila \n \
Привет, роднуля, ты думаешь я тут от нехуй делать сижу? Проходи.\
1. Представься, расскажи о себе.\
2. Уважай всех участников конфы.\
3. Долго молчишь - вылетаешь.\
4. Не ходишь на сходки - получаешь дурную славу.\
5. Еда богов - Гирос. Напиток богов - кофе.\
6. Тян можешь искать в других конфах, мы тут увожаемые люди.\
Добро пожаловать."


class Chatter(Model):
    username = CharField(unique=True)
    stat = IntegerField()

    class Meta:
        database = db


class GayDates(Model):
    date = DateField(unique=True)
    gay_name = CharField()

    class Meta:
        database = db


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
