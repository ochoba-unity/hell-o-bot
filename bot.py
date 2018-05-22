from cfg import *

bot = telebot.TeleBot(TOKEN)
check_users()


@bot.message_handler(commands=['ping'])
def welcome(message):
    bot.reply_to(message, "Пингуй лучше @pbsphp")


# Adds new guys
@bot.message_handler(content_types=['new_chat_member'])
def add(message):
    all_users = read_users()
    for i in all_users:
        if i.username == message.new_chat_member.username:
            i.present = 1
            bot.send_message(message.chat.id, "Добро пожаловать. Снова")
            dump(all_users)
            return
    all_users.append(Chatter(username=message.new_chat_member.username, present=1))
    dump(all_users)
    bot.send_message(message.chat.id, rules)
    bot.send_photo(message.chat.id, hello_image)


@bot.message_handler(commands=['all', 'ALL'])
def ping_all(message):
    all_users = read_users()
    answer = ""
    for i in all_users:
        if i.present:
            answer += "@" + i.username + "\n"
    bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['add_me'])
def add_me(message):
    all_users = read_users()
    for i in all_users:
        if i.username == message.from_user.username:
            bot.send_message(message.chat.id, "Ты уже есть")
            return
    all_users.append(Chatter(username=message.from_user.username, present=1))
    dump(all_users)
    bot.send_message(message.chat.id, "Добавила")


@bot.message_handler(content_types=['left_chat_member'])
def delete(message):
    all_users = read_users()
    for i in all_users:
        if i.username == message.left_chat_member.username:
            i.present = 0
    chatter_list = open(file="users.json", mode="w")
    json.dump(all_users, fp=chatter_list, cls=ChatterEncoder)
    chatter_list.close()


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


def dump(user_list):
    chatter_list = open(file="users.json", mode="w")
    json.dump(user_list, fp=chatter_list, cls=ChatterEncoder)
    chatter_list.close()


while True:
    try:
        bot.polling()
    finally:
        time.sleep(1)
