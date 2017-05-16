#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bot.py
#
#  Copyright 2017 user
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
import requests
import time
import urllib.request
import requests
from html.parser import HTMLParser
import os

offset = 0 # параметр необходим для подтверждения обновления
INTERVAL = 3 # Интервал проверки наличия новых сообщений (обновлений) на сервере в секундах
URL = 'https://api.telegram.org/bot' # URL на который отправляется запрос
TOKEN = '359373689:???????????????????????????????????' # токен вашего бота, полученный от @BotFather
data = {'offset': offset+1, 'limit': 0, 'timeout': 0}
debug = 0

def check_updates():
    """Проверка обновлений на сервере и инициация действий, в зависимости от команды"""
    global offset
    data = {'offset': offset + 1, 'limit': 5, 'timeout': 0} # Формируем параметры запроса

    try:
        request = requests.post(URL + TOKEN + '/getUpdates', data=data) # Отправка запроса обновлений
    except:
        print('Error getting updates') # Логгируем ошибку
        return False # Завершаем проверку

    if not request.status_code == 200: return False # Проверка ответа сервера
    if not request.json()['ok']: return False # Проверка успешности обращения к API
    for update in request.json()['result']: # Проверка каждого элемента списка
        offset = update['update_id'] # Извлечение ID сообщения
        # Ниже, если в обновлении отсутствует блок 'message'
        # или же в блоке 'message' отсутствует блок 'text', тогда
        if not 'message' in update or not 'text' in update['message']:
            print('Unknown update:\n%s' % update) # сохраняем в лог пришедшее обновление
            print('Iteration End.\n')
            print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n')
            continue # и переходим к следующему обновлению

        from_id = update['message']['chat']['id'] # Извлечение ID чата (отправителя)
        if not 'chat' in update['message'] or not 'username' in update['message']['from']:
            print('chat or username not found!:\n') # сохраняем в лог пришедшее обновление
            print('Iteration End.\n')
            print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n')
            continue # и переходим к следующему обновлению
        name = update['message']['from']['username'] # Извлечение username отправителя
        message = update['message']['text'] # Извлечение текста сообщения
        parameters = (offset, name, from_id, message)
        print('Message (id%s) from %s (id%s): "%s"' % parameters) # Вывод в лог ID и текста сообщения
        # В зависимости от сообщения, выполняем необходимое действие
        run_command(*parameters)


def run_command(offset, name, from_id, cmd):
    if cmd == '/w':
        send_text(from_id, '@'+name+', %s' % get_weather()) # Отправка ответа

    elif cmd == '/ping': # Ответ на ping
        send_text(from_id, '@'+name+', No route to host') # Отправка ответа

    elif cmd == '/help': # Ответ на help
        send_text(from_id, 'No help. No compassion. No mercy.') # Ответ

    elif cmd.startswith('/ping '):
        host=cmd[5:len(cmd)].strip()
        print('ping >'+host+'<')
        send_text(from_id, '@'+name+', %s' % ping(host)) # Отправка ответа

    #else:
    #    send_text(from_id, 'Got it.') # Отправка ответа


def send_text(chat_id, text):
    """Отправка текстового сообщения по chat_id
    ToDo: повторная отправка при неудаче"""
    print('Sending to %s: %s' % (chat_id, text)) # Запись события в лог
    data = {'chat_id': chat_id, 'text': text} # Формирование запроса
    request = requests.post(URL + TOKEN + '/sendMessage', data=data) # HTTP запрос
    if not request.status_code == 200: # Проверка ответа сервера
        return False # Возврат с неудачей
    return request.json()['ok'] # Проверка успешности обращения к API


def ping(hostname):
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        return hostname+" is up"
    else:
        return hostname+" is down"

class MyHTMLParser(HTMLParser):
    #def __init__(self):
    def reset(self):
        HTMLParser.reset(self)
        #HTMLParser.__init__(self)
        self.data = ''

    def handle_data(self, data):
        print("Encountered some data  :", data)
        self.data+=data+' '


def get_page(url):
    page = None
    r = requests.get(url)
    if r.status_code == 200:
        page = r.text
    return page

def get_weather():
    result=''
    w = get_page("http://www.tatarmeteo.ru/")
    index=w.find('<div class="pogoda"><h3>Текущая погода по г. Казани</h3>')
    if index != -1:
        w=w[index:len(w)]
        index=w.find('</table>')
        if index != -1:
            w=w[0:index]
            p=MyHTMLParser()
            p.feed(w)
            p.close()
            result = p.data
        return result
    else:
        return 'Weather not found!'


if __name__ == '__main__':
    import sys
    while True:
        try:
            check_updates()
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            print('Прервано пользователем..')
            break
    sys.exit(main(sys.argv))
