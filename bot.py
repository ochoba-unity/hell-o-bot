
import json
import datetime
import random
from random import randrange

import requests
from html.parser import HTMLParser
import os
import telebot
import time
from config import *

bot = telebot.TeleBot(token)


# Here could be your ads

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, мальчики")


@bot.message_handler(commands=['add_me'])
def new_member(message):
    if message.chat.id != main_chat_id:
        return
    all_names = get_all_names()
    for i in all_names:
        print(i)
        if i == message.from_user.username:
            bot.send_message(message.chat.id, "Ты уже есть в списке")
            return
    all_names.append(message.from_user.username)
    refresh_names(all_names)
    bot.send_message(message.chat.id, "Добавлен, теперь буду тебя пинговать")


@bot.message_handler(commands=['get_OCHOBA'])
def get_all(request):
    if request.chat.id != main_chat_id:
        return
    usernames = get_all_names()
    message = ""
    for name in usernames:
        message += "@" + name + " "
    bot.send_message(request.chat.id, message)


@bot.message_handler(content_types=['new_chat_member'])
def say_hello(message):
    if message.chat.id != main_chat_id:
        return
    bot.send_message(message.chat.id, chat_rules)  # chat_rules from config
    image = open("faq_image.jpg", "rb")
    time.sleep(10)
    bot.send_photo(message.chat.id, image)


@bot.message_handler(content_types=['left_chat_member'])
def delete(message):
    if message.chat.id != main_chat_id:
        return
    left_username = message.from_user.username
    all_names = get_all_names()
    for name in all_names:
        if name == left_username:
            all_names.remove(name)
            refresh_names(all_names)
            bot.send_message(message.chat.id, "Из пингов удалил")
            return

    bot.send_message(message.chat.id, "Его не было в листе пингов или что-то пошло не так")


@bot.message_handler(commands=['ping'])
def ping(hostname):
    print("Chat name = " + hostname.chat.title)
    print("Chat id = " + str(hostname.chat.id))

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


@bot.message_handler(commands=['pidoreg'])
def pidoreg(message):
    """
    Регистрирует пользователя в списке пидоров.
    Пидор локален для каждой конфы. Информация хранится по следующей
    схеме:
    {chat_id1:
        {current: {date: YYYY-MM-DD, username: TommyFontaine},
         stats: {username: count, username2: count, ...}},
     chat_id2: ...}.
    """
    chat_id = str(message.chat.id)
    username = message.from_user.username
    if not username:
        bot.reply_to(message, 'А у тебя юзернейма нет')
        return

    all_data = load_pidors()
    if chat_id not in all_data:
        all_data[chat_id] = {'current': {}, 'stats': {}}

    if username in all_data[chat_id]['stats']:
        bot.reply_to(message, 'Ты уже в игре')
        return

    all_data[chat_id]['stats'][username] = 0
    dump_pidors(all_data)
    bot.reply_to(message, 'Теперь ты в игре')


@bot.message_handler(commands=['pidorstats'])
def pidorstats(message):
    """
    Статистика по пидорам конфы.
    """
    chat_id = str(message.chat.id)
    all_data = load_pidors()
    if chat_id not in all_data:
        bot.reply_to(message, 'В этой хате пидоров нет')
        return

    stats = all_data[chat_id]['stats']
    rows = ['{} - {} раз(а)'.format(u, c) for u, c in stats.items()]
    bot.reply_to(message, '\n'.join(rows))


@bot.message_handler(commands=['pidor'])
def pidor(message):
    """
    Розыгрыш пидора дня.
    """
    chat_id = str(message.chat.id)
    all_data = load_pidors()
    if chat_id not in all_data:
        bot.reply_to(message, 'В этой хате пидоров нет')
        return

    today = datetime.date.today().isoformat()
    current = all_data[chat_id]['current']
    if current and current['date'] == today:
        bot.reply_to(
            message, 'Пидор дня - {}'.format(current['username']))
        return

    bot.reply_to(message, random.choice(search_for_pidor_replies))
    time.sleep(3)  # интрига

    candidates = all_data[chat_id]['stats']
    winner = random.choice(list(candidates.keys()))
    all_data[chat_id]['stats'][winner] += 1
    all_data[chat_id]['current'] = {'date': today, 'username': winner}

    # FIXME: Вот здесь могут быть проблемы, т.к. информация сериализуется
    # целиком в один файл, при этом не лочится. Необходимо запилить
    # мьютекс на всю эту функцию.
    dump_pidors(all_data)

    msg = random.choice(pidor_found_replies)
    bot.reply_to(message, msg.format(winner))


def load_pidors():
    with open('pidors.json', 'r') as f:
        data = json.load(f)
    return data


def dump_pidors(data):
    with open('pidors.json', 'w') as f:
        json.dump(data, f)


def check_if_reply(message):
    # checks if something was said to bot
    if message.reply_to_message:
        if message.reply_to_message.from_user.username == bot_username[1:]:
            return True
    return False


class MyHTMLParser(HTMLParser):
    def reset(self):
        HTMLParser.reset(self)
        self.data = ''

    def handle_data(self, data):
        self.data += data + ' '


class Stat:
    name = ""
    record = 0

    def __init__(self, name, record):
        self.name = name
        self.record = record


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
    #    try:
    bot.polling(none_stop=True)
# except:
#        print('\n \n')
#        print("**************************************************************************************")
#        print("Connection lost or any other error while bot polling, waiting 6 minutes and continue")
#        print("**************************************************************************************")
#        print('')
#        time.sleep(360)
