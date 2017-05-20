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


@bot.message_handler(content_types=['new_chat_member'])
def say_hello(message):
    bot.send_message(message.chat.id, chat_rules)  # chat_rules from config
    image = open("faq_image.jpg", "rb")
    time.sleep(10)
    bot.send_photo(message.chat.id, image)


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


@bot.message_handler(func=lambda message: check(message))
def reply(message):
    bot.reply_to(message, "Нет, ты")


def check(message):
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
