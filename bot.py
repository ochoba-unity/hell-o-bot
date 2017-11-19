from cfg import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "ddd")


@bot.message_handler(content_types=['new_chat_members'])
def add(message):
    bot.send_message(message.chat.id, rules)
    for newbie in message.new_chat_members:
        Chatter.create(username=newbie.username, stat=0)
    bot.send_photo(message.chat.id, hello_image)


@bot.message_handler(commands=['getall'])
def getall(message):
    answer = ""
    print("I got a message")
    for user in Chatter.select().order_by(-Chatter.stat):
        answer += "@" + str(user.username) + " был пидором " + str(user.stat) + " раз." + "\n"
    bot.reply_to(message, answer)


@bot.message_handler(commands=['history'])
def histoty(message):
    ans = ""
    for i in GayDates.select().order_by(GayDates.date):
        ans += f"{i.date} {i.gay_name} \n"
    bot.send_message(message.chat.id, f"Все пидоры за всё время\n + {ans}")


@bot.message_handler(commands=["pidor"])
def pidor(message):
    last_date = list(GayDates.select().order_by(-GayDates.date))[0]
    if last_date.date == date.today():
        bot.send_message(message.chat.id, f"Весь день сегодня Пидор дня - @{last_date.gay_name}.")
    else:
        everyone = Chatter.select()
        new_pidor = randint(0, len(everyone) - 1)
        GayDates.create(date=date.today(), gay_name=everyone[new_pidor].username)
        bot.send_message(message.chat.id, f"Новый Пидор дня - @{everyone[new_pidor].username}")


@bot.message_handler(commands=['all'])
def all(message):
    answer = ""
    for user in Chatter.select():
        answer += "@" + user.username + "\n"
    bot.reply_to(message, answer)


@bot.message_handler(commands=['add_me'])
def add_exist(message):
    try:
        if Chatter.get(Chatter.username == message.from_user.username):
            pass
    except DoesNotExist:
        Chatter.create(username=message.from_user.username, stat=0)
        bot.reply_to(message, "Добавила")
        return
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
    time.sleep(400)
