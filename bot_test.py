from telebot import TeleBot, types

bot = TeleBot('5694054533:AAGVrj58icZPu0L0_3XEVwa3pP1tLO1TGkU')

kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='test', web_app=types.WebAppInfo(url='https://5d1d-94-25-190-82.ngrok-free.app')))

bot.send_message(5061120370, 'test', reply_markup=kb)