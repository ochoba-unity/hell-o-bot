import requests
from html.parser import HTMLParser
import os
import telebot
import time
from config import *

bot = telebot.TeleBot(token)


# Проблемы с доступом в joy-casino.com ?

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, мальчики")


@bot.message_handler(commands=['add_me'])
def new_member(message):
    all_names = get_all_names()
    for i in all_names:
        print(i)
        if i == message.from_user.username:
            bot.send_message(message.chat.id, "Ты уже есть в списке")
            return
    all_names += message.from_user.username
    refresh_names(all_names)
    bot.send_message(message.chat.id, "Добавлен, теперь буду тебя пинговать")


@bot.message_handler(commands=['get_OCHOBA'])
def get_all(request):
    usernames = get_all_names()
    message = ""
    for name in usernames:
        message += "@" + name + " "
    bot.send_message(request.chat.id, message)


@bot.message_handler(content_types=['new_chat_member'])
def say_hello(message):
    bot.send_message(message.chat.id, chat_rules)  # chat_rules from config
    image = open("faq_image.jpg", "rb")
    time.sleep(10)
    bot.send_photo(message.chat.id, image)


@bot.message_handler(content_types=['left_chat_member'])
def delete(message):
    left_username = message.from_user.username
    all_names = get_all_names()
    for name in all_names:
        if name == left_username:
            name = None
            bot.send_message(message.chat.id, "Из пингов удалил")
            return

    bot.send_message(message.chat.id, "Его не было в листе пингов или что-то пошло не так")


@bot.message_handler(commands=['ping'])
def ping(hostname):
    response = os.system("ping -n 1 " + hostname.text[6:])
    if response == 0:
        bot.send_message(hostname.chat.id, hostname.text[6:] + " is up")
    else:
        bot.send_message(hostname.chat.id, hostname.text[6:] + " is down")


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


@bot.message_handler(func=lambda message: check_if_reply(message))
def reply(message):
    bot.reply_to(message, "Нет, ты")


def check_if_reply(message):
    # checks if something was said to bot
    if message.reply_to_message:
        if message.reply_to_message.from_user.username == bot_username:
            return True
    return False


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


def get_all_names():
    take = open("usernames.txt", "r")
    all_names = [s.strip('\n') for s in take]
    return all_names


def refresh_names(new_usernames):
    give = open("usernames.txt", "w")
    print("\n".join(new_usernames), file=give)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except:
        print('\n \n')
        print("**************************************************************************************")
        print("Connection lost or any other error while bot polling, waiting 6 minutes and continue")
        print("**************************************************************************************")
        print('')
        time.sleep(360)
