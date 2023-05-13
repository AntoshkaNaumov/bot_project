import telebot
import webbrowser
from telebot import types
from currency_converter import CurrencyConverter
import sqlite3
import requests
import json

bot = telebot.TeleBot('5608147379:AAH8tl9rt1CdxlKwH9nRemLzaqj0HT7Gi3c')
currency = CurrencyConverter()
name = None
amount = 0
API = '0889d09733553d0ae6817ee47a091c9e'


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users'
    ' (id int auto_increment primary key, name varchar(50), pass varchar(50) )')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет, сейчас Вас '
    'зарегистрируем! Введите Ваше имя')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей чата', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup=markup)

# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#    conn = sqlite3.connect('base.sql')
#    cur = conn.cursor()

#    cur.execute("SELECT * FROM users")
#    users = cur.fetchall()
#    info = ''
#    for element in users:
#        info += f'Имя: {element[1]}, пароль: {element[2]}\n'
#    cur.close()
#    conn.close()

#    bot.send_message(call.message.chat.id, info)


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Перейти на сайт')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Удалить фото')
    btn3 = types.KeyboardButton('Изменить текст')
    markup.row(btn2, btn3)
    file = open('./photo.jpg', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    # bot.send_message(message.chat.id, 'start menu', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'Перейти на сайт':
        webbrowser.open('https://www.google.com/')
        bot.send_message(message.chat.id, 'website is open')


@bot.message_handler(commands=['currency'])  # конвертер валют
def get_currency(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму для обмена')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Впишите сумму')
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше за 0. Впишите сумму')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через / ')
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так. Впишите значение заново')
        bot.register_next_step_handler(message, my_currency)


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('http://portfolio-anton-n.tilda.ws/')
    bot.send_message(message.chat.id, 'website is open')


@bot.message_handler(commands=['hello'])
def main(message):
    bot.send_message(message.chat.id, f'Приветствую,'
                                      f' {message.from_user.first_name} {message.from_user.last_name}!')


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>Help</b> <em><u>information</u></em>', parse_mode='html')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Доброго времени суток,'
                                          f' {message.from_user.first_name} {message.from_user.last_name}!')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='http://portfolio-anton-n.tilda.ws/')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn2, btn3)
    bot.reply_to(message, 'Какое классное фото!', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Изменненый текст', callback.message.chat.id, callback.message.message_id)


@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, 'Привет, рад Вас видеть!'
                                    'Напишите название города')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Сейчас погода: {temp}')

        image = '1.png' if temp > 5.0 else '2.jpg' if 5.0 > temp > 0 else '3.png'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, 'Город указан не верно')


bot.infinity_polling(none_stop=True)
