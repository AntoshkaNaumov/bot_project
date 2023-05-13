from aiogram import Bot, Dispatcher, executor, types


bot = Bot('5742777204:AAH8RflW8JFx43DFqK54Spl2xx3JBe5_ViI')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # await bot.send_message(message.chat.id, 'Hello')
    await message.answer('Hello, how are you?')


@dp.message_handler(content_types=['photo'])
async def start(message: types.Message):
    await message.answer('Cool photo')


@dp.message_handler(content_types=['vodeo'])
async def start(message: types.Message):
    await message.answer('Cool video')


#@dp.message_handler(content_types=['text'])
#async def start(message: types.Message):
#    #await message.answer('Рад знакомству с тобой. Расскажи о себе')
#    await message.reply('Рад знакомству с тобой. Расскажи о себе.')
#    file = open('/photo.jpg', 'rb')
#    await message.answer_photo(file)


@dp.message_handler(commands=['inline'])
async def info(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Site', url='https://fotostrana.ru/superanton/'))
    markup.add(types.InlineKeyboardButton('Hello', callback_data='hello'))
    await message.reply('Hello', reply_markup=markup)


@dp.callback_query_handler()
async def callback(call):
    await call.message.answer(call.data)


@dp.message_handler(commands=['reply'])
async def reply(message: types.Message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton('Site'))
    markup.add(types.KeyboardButton('Website'))
    await message.answer('Hello', reply_markup=markup)


executor.start_polling(dp)
