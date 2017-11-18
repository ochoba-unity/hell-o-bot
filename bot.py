from html.parser import HTMLParser

import requests
import telebot
from cfg import *

bot = telebot.TeleBot(TOKEN)
db.connect()
try:
    db.create_table(Chatter)
except:
    pass


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "ddd")


@bot.message_handler(content_types=['new_chat_members'])
def add(message):
    bot.send_message(message.chat.id, rules)
    for newbie in message.new_chat_members:
        Chatter.create(username=newbie.username, gay=0)
    bot.send_photo(message.chat.id, hello_image)


@bot.message_handler(commands=['getall'])
def getall(message):
    answer = ""
    for user in Chatter.select():
        answer += "@" + str(user.username) + " был пидором" + str(user.gay) + " раз." + "\n"
    bot.reply_to(message, answer)


@bot.message_handler(commands=['add_me'])
def add_exist(message):
    try:
        if not Chatter.get(Chatter.username == message.from_user.username):
            Chatter.create(username=message.from_user.username, gay=0)
            bot.reply_to(message, "Добавила")
            return
    except DoesNotExist:
        pass
    bot.reply_to(message, "Ты уже есть")


@bot.message_handler(content_types=['left_chat_member'])
def remove(message):
    try:
        user = Chatter.get(Chatter.username == message.left_chat_member.username)
        user.delete_instance()
        bot.reply_to(message, "Удалила")
    except:
        pass
    bot.reply_to(message, "¯\_(ツ)_/¯")


@bot.message_handler(commands=['w'])
def get_weather(message):
    result = ''
    w = get_page("http://www.tatarmeteo.ru/")
    index = w.find('<div class="pogoda"><h3>Текущая погода по г. Казани</h3>')
    if index != -1:
        w = w[index:len(w)]
        index = w.find('</table>')
        if index != -1:
            w = w[0:index]
            p = MyHTMLParser()
            p.feed(w)
            p.close()
            result = p.data
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, 'Weather not found!')


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


while True:
    bot.polling()
