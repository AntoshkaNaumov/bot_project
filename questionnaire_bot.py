import re

import telebot
from telebot import types
import sqlite3
from config import BOT_TOKEN


bot = telebot.TeleBot(BOT_TOKEN)
name = None
surname = None
age = 0
city = None
profession = None
language = None


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Заполнить анкету')
    markup.add(btn1)
    bot.send_message(message.chat.id, 'start menu', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'Заполнить анкету':

        conn = sqlite3.connect('questionnaire_base.sqlite')
        cur = conn.cursor()

        cur.execute('CREATE TABLE IF NOT EXISTS questionnaire'
        ' (id int auto_increment primary key, name varchar(50), surname varchar(50),'
        'age int, city varchar(50), profession varchar(50), language varchar(50), citizenship varchar(70))')
        conn.commit()
        cur.close()
        conn.close()

        bot.send_message(message.chat.id, '<b>Здравствуйте, сейчас Вам необходимо заполнить анкету для трудоустройства!'
                                          'Сначала введите Ваше имя</b>', parse_mode='html')
        bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    if bool(re.fullmatch(r'(?i)[а-яё]+', name)) == True:
        bot.send_message(message.chat.id, 'Введите Вашу фамилию')
        bot.register_next_step_handler(message, user_surname)
    else:
        bot.send_message(message.chat.id, 'Введите на русском языке')
        bot.register_next_step_handler(message, user_name)


def user_surname(message):
    global surname
    surname = message.text.strip()
    if bool(re.fullmatch(r'(?i)[а-яё]+', surname)) == True:
        bot.send_message(message.chat.id, 'Введите Ваш возраст')
        bot.register_next_step_handler(message, user_age)
    else:
        bot.send_message(message.chat.id, 'Введите на русском языке')
        bot.register_next_step_handler(message, user_surname)


def user_age(message):
    global age
    try:
        age = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Введите возраст')
        bot.register_next_step_handler(message, user_age)
    if 18 < age < 60:
        bot.send_message(message.chat.id, 'Введите Ваш город')
        bot.register_next_step_handler(message, user_city)
    else:
        bot.send_message(message.chat.id, 'Возраст должен быть больше 18 и меньше 60. Введите возраст')
        bot.register_next_step_handler(message, user_age)


def user_city(message):
    global city
    city = message.text.strip()
    if bool(re.fullmatch(r'(?i)[а-яё]+', city)) == True:
        bot.send_message(message.chat.id, 'Введите Вашу профессию')
        bot.register_next_step_handler(message, user_profession)
    else:
        bot.send_message(message.chat.id, 'Введите на русском языке')
        bot.register_next_step_handler(message, user_city)


def user_profession(message):
    global profession
    profession = message.text.strip()
    if bool(re.fullmatch(r'(?i)[а-яё]+', profession)) == True:
        bot.send_message(message.chat.id, 'Введите Ваш язык')
        bot.register_next_step_handler(message, user_language)
    else:
        bot.send_message(message.chat.id, 'Введите на русском языке')
        bot.register_next_step_handler(message, user_profession)


def user_language(message):
    global language
    language = message.text.strip()
    if bool(re.fullmatch(r'(?i)[а-яё]+', language)) == True:
        bot.send_message(message.chat.id, 'Введите Ваше гражданство')
        bot.register_next_step_handler(message, user_citizenship)
    else:
        bot.send_message(message.chat.id, 'Введите на русском языке')
        bot.register_next_step_handler(message, user_language)


def user_citizenship(message):
    citizenship = message.text.strip()
    if bool(re.fullmatch(r'(?i)[а-яё]+', citizenship)) == True:
        conn = sqlite3.connect('questionnaire_base.sqlite')
        cur = conn.cursor()

        cur.execute("INSERT INTO questionnaire (name, surname, age, city, profession, language, citizenship)"
    " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (name, surname, age, city, profession, language, citizenship
    ))
        conn.commit()
        cur.close()
        conn.close()
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Просмотр анкеты', callback_data='questionnaire'))
        bot.send_message(message.chat.id, 'Анкета заполнена', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Введите на русском языке')
        bot.register_next_step_handler(message, user_citizenship)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('questionnaire_base.sqlite')
    cur = conn.cursor()

    cur.execute("SELECT * FROM questionnaire")
    users = cur.fetchall()
    info = ''
    for element in users:
        info += f' Имя: {element[1]}, Фамилия: {element[2]},' \
                f' Возраст: {element[3]}\n Город: {element[4]}, Профессия: {element[5]}\n Язык: {element[6]},' \
                f' Гражданство: {element[7]}\n'
    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


bot.infinity_polling(none_stop=True)