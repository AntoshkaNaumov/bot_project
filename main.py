from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo


bot = Bot('5742777204:AAH8RflW8JFx43DFqK54Spl2xx3JBe5_ViI')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(url='https://itproger.com')))
    await message.answer('Привет мой друг!', reply_markup=markup)


executor.start_polling(dp)
