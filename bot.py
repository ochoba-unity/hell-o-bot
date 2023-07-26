from cfg import *

bot = telebot.TeleBot(TOKEN)
check_users()

# ping command
@bot.message_handler(commands=['ping'])
def welcome(message):
    bot.reply_to(message, "Bot is up!")


# Adds new guys
@bot.message_handler(content_types=['new_chat_members'])
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

# Ping everyone in the chat
@bot.message_handler(commands=['all', 'ALL'])
def ping_all(message):
    all_users = read_users()
    answer = ""
    for user in all_users:
        if user.present:
            answer += "@" + i.username + "\n"
    if answer != "":
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, "Никого нет!")

# Adds the user to chat members list
@bot.message_handler(commands=['add_me'])
def add_me(message):
    all_users = read_users()
    for user in all_users:
        if user.username == message.from_user.username:
            bot.send_message(message.chat.id, "Ты уже есть")
            return
    all_users.append(Chatter(username=message.from_user.username, present=1))
    dump(all_users)
    bot.send_message(message.chat.id, "Добавила")

# Delete left member
@bot.message_handler(content_types=['left_chat_members'])
def delete(message):
    all_users = read_users()
    for user in all_users:
        if user.username == message.left_chat_member.username:
            user.present = 0
    dump(all_users)
    bot.send_message(message.chat.id, "Удалила")

# Check the weather in Kazan
@bot.message_handler(commands=['weather'])
def get_weather(message):
    result = ''
    page = get_page("http://www.tatarmeteo.ru/")
    index = page.find('<div class="pogoda"><h3>Текущая погода по г. Казани</h3>')
    if index != -1:
        page = page[index:len(w)]
        index = page.find('</table>')
        if index != -1:
            page = w[0:index]
            parser = MyHTMLParser()
            parser.feed(page)
            parser.close()
            result = parser.data
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, 'Weather not found!')




while __name__ == "bot":
    try:
        bot.polling()
    finally:
        time.sleep(1)
