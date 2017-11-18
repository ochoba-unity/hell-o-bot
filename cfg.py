from peewee import *

db = SqliteDatabase("database.sql")
TOKEN = ""
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
    gay = IntegerField()

    class Meta:
        database = db
