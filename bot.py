from cfg import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['ping'])
def welcome(message):
    bot.reply_to(message, "Пингуй лучше @pbsphp")


# Adds new guys
@bot.message_handler(content_types=['new_chat_members'])
def add(message):
    for newbie in message.new_chat_members:
        try:
            update = Chatter.get(Chatter.username == newbie.username)
            update.in_chat = True
            update.save()
            bot.send_message(message.chat.id, "Добро пожаловать. Снова")
        except peewee.DoesNotExist:
            Chatter.create(username=newbie.username, stat=0)
            bot.send_message(message.chat.id, rules)
            bot.send_photo(message.chat.id, hello_image)


# Adds a guy if he wants
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


# Show all pidors with stats
@bot.message_handler(commands=['getall'])
def getall(message):
    answer = ""
    print("I got a message")
    for user in Chatter.select().order_by(-Chatter.stat):
        answer += "@" + str(user.username) + " был кем-то " + str(user.stat) + " раз." + "\n"
    bot.reply_to(message, answer)


# Show all pidors with dates
@bot.message_handler(commands=['history'])
def history(message):
    ans = ""
    for i in GayDates.select().order_by(GayDates.date):
        ans += f"{i.date} {i.gay_name} \n"
    bot.send_message(message.chat.id, f"Все пидоры за всё время\n{ans}")


# Tell who is pidor today
@bot.message_handler(commands=["pidor"])
def pidor(message):
    last_date = list(GayDates.select().order_by(-GayDates.date))[0]
    if last_date.date == date.today():
        bot.send_message(message.chat.id, f"Весь день сегодня {last_date.status} дня - @{last_date.gay_name}.")
    else:
        everyone = Chatter.select()
        new_pidor = randint(0, len(everyone) - 1)
        GayDates.create(date=date.today(), gay_name=everyone[new_pidor].username)
        update = Chatter.get(Chatter.username == everyone[new_pidor].username)
        status = lucky_names[randint(0, len(lucky_names) - 1)]
        bot.send_message(message.chat.id, "Кого заведём себе сегодня?")
        time.sleep(4)
        update.stat += 1
        action = actions[randint(0, len(actions) - 1)]
        bot.send_message(message.chat.id, action)
        time.sleep(4)
        stat_update = GayDates.get(GayDates.date == date.today())
        stat_update.status = status
        stat_update.save()
        update.save()

        bot.send_message(message.chat.id,
                         f"Короче новый(ая) {status} дня - @{everyone[new_pidor].username}")


# ping everyone
@bot.message_handler(commands=['all'])
def all(message):
    answer = ""
    for user in Chatter.select():
        if user.in_chat:
            answer += "@" + user.username + "\n"
    bot.reply_to(message, answer)


# Delete guy if he left. This makes bot no longer ping a guy until he's returned
# but keeps his data
@bot.message_handler(content_types=['left_chat_member'])
def remove(message):
    try:
        user = Chatter.get(Chatter.username == message.left_chat_member.username)
        user.in_chat = False
        user.save()
        bot.reply_to(message, "Удалила")
    except:
        pass
    bot.reply_to(message, "¯\_(ツ)_/¯")


@bot.message_handler(commands=['set'])
def set(message):
    text = message.text[4:].split()
    StringHolder.create(key=text[0], value=text[1])
    bot.send_message(message.chat.id, f"Гет {text[0]} создан")


@bot.message_handler(commands=['del'])
def delete(message):
    text = message.text[4:].split()
    print(text)
    try:
        deleting = StringHolder.get(StringHolder.key == text[0])
        deleting.delete_instance()
    except TypeError:
        bot.send_message(message.chat.id, "Нет такого гета")
        return
    bot.send_message(message.chat.id, f"Гет {text[0]} удалён")


@bot.message_handler(commands=['get'])
def get(message):
    key = message.text[4:].split()
    print(key)
    # try:
    ans = StringHolder.get(StringHolder.key == key).value
    bot.send_message(message.chat.id, ans)
    # except Exception:
    #    bot.send_message(message.chat.id, "Нет такого ключа")


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
    try:
        bot.polling()
    finally:
        time.sleep(1)
