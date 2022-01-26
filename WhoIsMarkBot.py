import telebot
import sqlite3

bot = telebot.TeleBot('5074611111:AAGTe9obDrVSuL55jnuOYHAetHHmjEDiHnU')
conn = sqlite3.connect('/home/valentine/Desktop/PycharmProjects/telegrambot/db_message', check_same_thread=False)
cursor = conn.cursor()


@bot.message_handler(['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Че приперся, кожаный?')


def db_insert(user_id: int, message: str, user_name: str):
    cursor.execute('INSERT INTO telebot_messages (user_id, message, user_name) VALUES (?, ?, ?)',
                   (user_id, message, user_name))
    conn.commit()


def db_insert_active(user_id: int):
    cursor.execute('INSERT INTO user_active (user_id, activity) VALUES (?, ?)',
                   (user_id, 1))
    conn.commit()


def db_get(user_id: int):
    cursor.execute('select message from telebot_messages where user_id = {} limit 1'.format(str(user_id)))
    result = cursor.fetchall()
    return str(result[-1][-1])


def check_play(user_id: int) -> bool:
    cursor.execute('select activity from user_active where user_id = {} limit 1'.format(str(user_id)))
    result = cursor.fetchall()
    return result


@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_text_messages(message):
    if check_play():
        bot.send_message(message.from_user.id, db_get(1))  ######

    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.from_user.id, 'Вечер в хату, чем я могу тебе помочь, кожаный?')

    elif message.text == "/help":
        bot.send_message(message.from_user.id, 'Напиши "Хочу играть", кожаный')

    elif message.text == 'Хочу играть':
        bot.send_message(message.chat.id, 'Ща я тебе расскажу правила')
        bot.send_message(message.chat.id, 'Это игра в которой тебе нужно отгадать с кем ты играешь во время общения, при этом категорически нельзя называть свое имя')
        bot.send_message(message.chat.id, 'Погнали?')
        bot.send_message(message.chat.id, 'Напиши "/play" и мы начнем)))')

    elif message.text == 'Погнали':
        db_insert(message.from_user.id, '', message.from_user.first_name)
        bot.send_message(message.from_user.id, str(db_get(message.from_user.id)))

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю, кожаный. Напиши /help.")


bot.polling(none_stop=True, interval=0)
