# import time
# import urllib.request
import requests
from html.parser import HTMLParser
import os
import telebot
from config import *

bot = telebot.TeleBot(token)


# Проблемы с доступом в joy-casino.com ?

@bot.message_handler(content_types=['new_chat_member'])
def say_hello(message):
    bot.send_message(message.chat.id, chat_rules)  # chat_rules from config


@bot.message_handler(commands=['ping'])
def ping(hostname):
    response = os.system("ping -c 1 " + hostname.text[6:])
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


class MyHTMLParser(HTMLParser):
    # def __init__(self):

    def reset(self):
        HTMLParser.reset(self)
        # HTMLParser.__init__(self)
        self.data = ''

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        self.data += data + ' '


def get_page(url):
    r = requests.get(url)
    if r.status_code == 200:
        page = r.text
    return page


if __name__ == '__main__':
    bot.polling(none_stop=True)
